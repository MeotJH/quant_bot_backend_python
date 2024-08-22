import requests
import yfinance as yf
import pandas as pd
import json
import os
import json
from datetime import datetime

from api.stock.models import Stock


def find_stocks():
    external_api_url ="https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(external_api_url, headers=headers)
    stocks = []
    if response.status_code == 200:
        # JSON 데이터를 파싱합니다.
        stocks_json = response.json()['data']['rows']
        for stock_dict in stocks_json:
            stock = Stock(stock_dict)
            stocks.append(stock)

    sorted_objects = sorted(stocks, key=lambda x: float(x.market_cap) if x.market_cap else 0.0, reverse=True)
    return sorted_objects




# def find_stocks():
#
#     # 파일 이름 정의
#     filename = 'stock_data.json'
#
#     # 파일이 존재하고, 수정일자가 오늘이라면 로직 패스
#     if _is_file_stock_date_equal(filename):
#         print(f"{filename} is up-to-date. Skipping the rest of the logic.")
#         with open(filename, 'r') as file:
#             stock_json = json.load(file)
#         return stock_json
#
#     # S&P 500 티커 리스트 가져오기
#     sp500_tickers = _get_sp500_tickers()
#     # 유효한 티커 필터링
#     valid_tickers = _validate_tickers(sp500_tickers)
#     # 유효한 티커로 데이터 다운로드
#     stock_data = _download_stock_data(valid_tickers)
#     # 데이터를 JSON 형식으로 변환
#     stock_json = _convert_to_json(stock_data, valid_tickers)
#     # JSON 객체 그대로 반환
#     _save_json_to_file(stock_json, 'stock_data.json')
#     return stock_json


def find_stock_by_id(item_id, period='1y', trend_follow_days=75):

    # 주식 데이터를 최근 100일간 가져옴
    stock_data = yf.Ticker(item_id).history(period=period)

    stock_data = stock_data.sort_index(ascending=False)
    # 75일 이동평균선 계산
    stock_data['75_MA'] = stock_data['Close'].rolling(window=trend_follow_days).mean()

    stock_data = stock_data.sort_index(ascending=True)

    # 결과를 딕셔너리 형태로 변환하여 반환
    stocks_dict = stock_data.reset_index().to_dict(orient='records')
    for stock in stocks_dict:
        stock['Date'] = stock['Date'].strftime('%Y-%m-%d')

    return stocks_dict


def _is_file_stock_date_equal(filename):
    if not os.path.exists(filename):
        return False

    with open(filename, 'r') as file:
        data = json.load(file)
        # 파일의 수정일자 가져오기
        aapl = data['AAPL']
        file_stock_date = aapl['Date']
        last_market_date = get_last_market_date().strftime('%Y-%m-%d')

    return file_stock_date == last_market_date


def get_last_market_date(ticker_symbol='AAPL'):
    ticker = yf.Ticker(ticker_symbol)
    # '1d' 기간 동안의 주식 데이터를 가져옵니다.
    history_data = ticker.history(period='1d', interval='1d')

    if not history_data.empty:
        # 마지막 거래일의 날짜를 가져옵니다.
        last_market_date = history_data.index[-1].date()
        return last_market_date
    else:
        return None


def _get_sp500_tickers(url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'):
    sp500_table = pd.read_html(url)
    sp500_df = sp500_table[0]
    return sp500_df['Symbol'].tolist()


def _validate_tickers(tickers):
    valid_tickers = []
    for ticker in tickers:
        try:
            stock_info = yf.Ticker(ticker).history(period='1d')
            if not stock_info.empty:
                valid_tickers.append(ticker)
        except Exception as e:
            print(f"Error with ticker {ticker}: {e}")
    return valid_tickers


def _download_stock_data(valid_tickers):
    return yf.download(valid_tickers, period='1d', group_by='ticker')


def _convert_to_json(stock_data, valid_tickers):
    result = {}
    for ticker in valid_tickers:
        ticker_data = stock_data[ticker].reset_index()
        # Timestamp를 문자열로 변환
        ticker_data['Date'] = ticker_data['Date'].astype(str)
        ticker_data_dict = ticker_data.to_dict(orient='records')

        # 데이터가 단일 행인 경우 리스트 대신 딕셔너리로 저장
        if len(ticker_data_dict) == 1:
            result[ticker] = ticker_data_dict[0]
        else:
            result[ticker] = ticker_data_dict
    return result


def _save_json_to_file(json_data, filename):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)