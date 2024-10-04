import requests


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



