from numbers import Number

from api.quant.model import QuantData
import yfinance as yf
from flask_jwt_extended import get_jwt_identity

from api import db
from api.quant.entityies import Quant
from api.user.entities import User
from exceptions import BadRequestException
from exceptions import BadRequestException


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


def register_quant_by_stock(stock: str, quant_data: QuantData):
    jwt_user = get_jwt_identity()
    user = User.query.filter_by(email=jwt_user).first()

    quant = Quant.query.filter_by(stock=stock, user_id=user.uuid, quant_type=quant_data.quant_type ).first()

    if quant is not None:
        raise BadRequestException('이미 존재하는 퀀트입니다.', 400)

    if user is None:
        return {"error": "User not found"}

    new_quant = Quant(
        stock=stock,
        quant_type=quant_data.quant_type,
        initial_price=quant_data.initial_price,
        initial_trend_follow=quant_data.initial_trend_follow,
        initial_status=quant_data.initial_status,
        current_status=quant_data.initial_status,
        notification=True,
        user_id=user.uuid
    )

    try:
        db.session.add(new_quant)
        db.session.commit()
        return new_quant.to_dict()
    except Exception as e:
        db.session.rollback()
        raise BadRequestException(f'{e}', 400)

def find_quants_by_user():
    jwt_user = get_jwt_identity()
    user = User.query.filter_by(email=jwt_user).first()
    quants = Quant.query.filter_by(user_id=user.uuid).all()


    quants_dict = []
    for quant in quants:
        stock_id = quant.stock
        stock = find_stock_by_id(stock_id)
        recent_stock = stock["stock_info"]

        # 모델에서 가져온 값을 가정
        previous_close = float(recent_stock['previousClose'])  # 모델에서 previousClose 값을 가져옴
        last_cross_trend_follow = float(recent_stock['lastCrossTrendFollow'])  # 모델에서 lastCrossTrendFollow 값을 가져옴

        # 수익 및 수익률 계산
        profit = previous_close - last_cross_trend_follow
        profit_percent = (profit / previous_close) * 100

        # 결과 출력
        quant_one = {
            "id": quant.uuid,
            "ticker": stock_id,
            "name": stock["stock_info"]["longName"],
            "profit": round(profit, 2),
            "profit_percent":  round(profit_percent, 2),
            "notification" : quant.notification,
            "quant_type" : quant.quant_type,
            "current_status" : quant.current_status,
            "initial_status" : quant.initial_status,
        }
        quants_dict.append(quant_one)

    return quants_dict

def patch_quant_by_id(quant_id):
    quant = Quant.query.filter_by(uuid=quant_id).first()
    if quant is None:
        raise BadRequestException('퀀트를 찾을 수 없습니다.', 400)
    quant.notification = not quant.notification
    db.session.commit()
    return quant.to_dict()
