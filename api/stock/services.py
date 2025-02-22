import requests
import subprocess
import json


from api.stock.models import Stock


def find_stocks():
    external_api_url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
    curl_command = [
        "curl",
        "-X", "GET",
        external_api_url,
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "-H", "Accept-Encoding: gzip, deflate, br",
        "-H", "Accept-Language: en-US,en;q=0.9",
        "-H", "Connection: keep-alive",
        "-H", "Upgrade-Insecure-Requests: 1",
        "--compressed"
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response_json = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during curl execution: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

    stocks = []
    try:
        stocks_json = response_json['data']['rows']
        for stock_dict in stocks_json:
            stock = Stock(stock_dict)
            stocks.append(stock)
    except KeyError as e:
        print(f"Error parsing stock data: {e}")
        return []

    print(f'가져온건 이거여 {stocks[0]}')
    sorted_objects = sorted(stocks, key=lambda x: float(x.market_cap) if x.market_cap else 0.0, reverse=True)
    return sorted_objects


# def find_stocks():
#     external_api_url ="https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true"
#     headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1"
#     }
#     response = requests.get(external_api_url, headers=headers)
#     stocks = []
#     if response.status_code == 200:
#         # JSON 데이터를 파싱합니다.
#         stocks_json = response.json()['data']['rows']
#         for stock_dict in stocks_json:
#             stock = Stock(stock_dict)
#             stocks.append(stock)

#     print(f'가져온건 이거여 {stocks[0]}')
#     sorted_objects = sorted(stocks, key=lambda x: float(x.market_cap) if x.market_cap else 0.0, reverse=True)
#     return sorted_objects



