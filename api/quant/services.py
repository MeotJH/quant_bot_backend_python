import yfinance as yf

def find_stock_by_id(item_id, period='1y', trend_follow_days=75):

    # 주식 데이터를 최근 100일간 가져옴
    stock_data = yf.Ticker(item_id).history(period=period)

    #stock_data = stock_data.sort_index(ascending=T)
    # 75일 이동평균선 계산
    stock_data['Trend_Follow'] = stock_data['Close'].rolling(window=trend_follow_days).mean()

    stock_data = stock_data.sort_index(ascending=False)
    stock_data = stock_data.dropna(subset=['Trend_Follow'])
    # 결과를 딕셔너리 형태로 변환하여 반환
    stocks_dict = stock_data.reset_index().to_dict(orient='records')
    for stock in stocks_dict:
        stock['Date'] = stock['Date'].strftime('%Y-%m-%d')

    return stocks_dict