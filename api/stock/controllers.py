import json
from dataclasses import asdict

from flask_restx import Resource, fields

from api import stock_api as api


from api.stock.services import find_stocks


stock_model = api.model('StockModel', {
    'symbol': fields.String(title='stock ticker'),
    'name': fields.String(title='stock name'),
    'lastsale': fields.String(title='stock price'),
    'netchange': fields.String(title='stock netchange'),
    'pctchange': fields.String(title='stock pctchange'),
    'volume': fields.String(title='stock volume'),
    'market_cap': fields.String(title='stock market_cap'),
    'country': fields.String(title='stock country'),
    'ipo_year': fields.String(title='stock ipo_year'),
    'industry': fields.String(title='stock industry'),
    'sector': fields.String(title='stock sector'),
    'url': fields.String(title='stock url'),
})

stocks_model = api.model('StocksModel', {
    'stocks': fields.List(fields.Nested(stock_model), required=True, description='stock 목록'),
})


@api.route('/', strict_slashes=False)
class Stocks(Resource):

    @api.marshal_with(stocks_model)
    def get(self):
        # item_id가 없을 경우 모든 stocks를 반환
        stocks = find_stocks()
        stocks_dict_list = [asdict(stock) for stock in stocks]
        return {'stocks': stocks_dict_list}


