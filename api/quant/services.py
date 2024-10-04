import yfinance as yf
from flask_jwt_extended import get_jwt_identity

from api import db
from api.quant.models import Quant
from api.user.model import User


def find_stock_by_id(item_id, period='1y', trend_follow_days=75):

    # 주식 데이터를 최근 period간 가져옴
    stock_data = yf.Ticker(item_id).history(period=period)
    stock_info = yf.Ticker(item_id).info

    # 75일 이동평균선 계산
    stock_data['Trend_Follow'] = stock_data['Close'].rolling(window=trend_follow_days).mean()

    # 마지막 교차점의 이동평균 값 가져오기
    last_cross_trend_follow = _find_last_cross_trend_follow(stock_data=stock_data)
    stock_info['lastCrossTrendFollow'] = last_cross_trend_follow

    stock_data = stock_data.sort_index(ascending=False)
    stock_data = stock_data.dropna(subset=['Trend_Follow'])
    # 결과를 딕셔너리 형태로 변환하여 반환
    stocks_dict = stock_data.reset_index().to_dict(orient='records')
    for stock in stocks_dict:
        stock['Date'] = stock['Date'].strftime('%Y-%m-%d')

    return {'stock_history' : stocks_dict, 'stock_info': stock_info}

def _find_last_cross_trend_follow(stock_data:dict):
    # 교차점 찾기: Close 값과 Trend_Follow 값의 차이의 부호가 바뀌는 지점 찾기
    stock_data['Prev_Close'] = stock_data['Close'].shift(1)
    stock_data['Prev_Trend_Follow'] = stock_data['Trend_Follow'].shift(1)
    # 교차 지점 판별 (부호가 바뀌는 지점)
    stock_data['Cross'] = (stock_data['Close'] > stock_data['Trend_Follow']) != (stock_data['Prev_Close'] > stock_data['Prev_Trend_Follow'])
    # 교차가 발생한 행 필터링
    cross_data = stock_data[stock_data['Cross'] & stock_data['Trend_Follow'].notnull()]
    if not cross_data.empty:
        last_cross_trend_follow = cross_data.iloc[-1]['Trend_Follow']
    else:
        last_cross_trend_follow = None
    
    return last_cross_trend_follow

def register_quant_by_stock(stock: str):
    # 1. User를 UUID를 통해 찾기
    jwt_user = get_jwt_identity()
    user = User.query.filter_by(uuid=jwt_user).first()

    if user is None:
        return {"error": "User not found"}

    # 2. Quant 객체 생성
    new_quant = Quant(
        stock=stock,
        notification=False,
        user_id=user.uuid  # user의 uuid를 외래키로 설정
    )

    # 3. 데이터베이스에 저장
    try:
        db.session.add(new_quant)
        db.session.commit()
        return {"success": "Quant saved successfully", "quant": new_quant.to_dict()}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to save Quant: {str(e)}"}
