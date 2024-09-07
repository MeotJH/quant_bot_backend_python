import yfinance as yf
import pandas as pd

# 파라미터 설정
item_id = "AAPL"  # 주식 코드
period = "1y"     # 데이터 기간 (예: 1년)
trend_follow_days = 75  # 이동평균선 일 수

# 주식 데이터 가져오기
stock_data = yf.Ticker(item_id).history(period=period)

# 75일 이동평균선 계산
stock_data['Trend_Follow'] = stock_data['Close'].rolling(window=trend_follow_days).mean()

# 교차점 찾기: Close 값과 Trend_Follow 값의 차이의 부호가 바뀌는 지점 찾기
stock_data['Prev_Close'] = stock_data['Close'].shift(1)
stock_data['Prev_Trend_Follow'] = stock_data['Trend_Follow'].shift(1)

# 교차 지점 판별 (부호가 바뀌는 지점)
stock_data['Cross'] = (stock_data['Close'] > stock_data['Trend_Follow']) != (stock_data['Prev_Close'] > stock_data['Prev_Trend_Follow'])

# 교차가 발생한 행 필터링
cross_data = stock_data[stock_data['Cross'] & stock_data['Trend_Follow'].notnull()]

# 교차한 가장 최근의 이동평균 값과 최신 Close 값 가져오기
if not cross_data.empty:
    last_cross_trend_follow = cross_data.iloc[-1]['Trend_Follow']  # 마지막 교차 지점의 이동평균선 값
    last_close = stock_data.iloc[-1]['Close']  # 가장 최신의 Close 값
    
    # 비교 결과 출력
    print(f"가장 최근 교차점에서의 이동평균 값: {last_cross_trend_follow}")
    print(f"가장 최근의 Close 값: {last_close}")
    
    if last_close > last_cross_trend_follow:
        print("가장 최근의 Close 값이 마지막 교차점의 이동평균 값보다 큽니다.")
    else:
        print("가장 최근의 Close 값이 마지막 교차점의 이동평균 값보다 작습니다.")
else:
    print("최근에 교차한 지점이 없습니다.")