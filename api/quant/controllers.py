from flask_jwt_extended import jwt_required
from flask_restx import fields, Resource

from api import quant_api as api
from api.quant.services import find_stock_by_id, register_quant_by_stock

trend_follow_model = api.model('TrendFollowModel', {
    'Date': fields.String(title='stock ticker'),
    'Open': fields.String(title='stock name'),
    'High': fields.String(title='stock price'),
    'Low': fields.String(title='stock netchange'),
    'Close': fields.String(title='stock pctchange'),
    'Volume': fields.String(title='stock volume'),
    'Dividends': fields.String(title='stock market_cap'),
    'Stock Splits': fields.String(title='stock country'),
    'Trend_Follow': fields.String(title='stock ipo_year'),
})

stock_info_model = api.model('StockInfoModel', {
    'shortName': fields.String(title='stock name'),
    'currentPrice': fields.String(title='Current Price'),
    'previousClose': fields.String(title='Previous Close'),
    'open': fields.String(title='Open'),
    'volume': fields.String(title='Volume'),
    'dayHigh': fields.String(title='stock High'),
    'dayLow': fields.String(title='stock Low'),
    'trailingPE': fields.String(title='per'),
    'fiftyTwoWeekHigh': fields.String(title='52High'),
    'fiftyTwoWeekLow': fields.String(title='52Low'),
    'trailingEps': fields.String(title='trailingEps'),
    'enterpriseValue': fields.String(title='Enterprise Value'),
    'ebitda' : fields.String(title='EBITDA'),
    'lastCrossTrendFollow': fields.String(title='Last Cross Trend Follow'),
})

trend_follows_model = api.model('TrendFollowsModel', {
    'stock_history': fields.List(fields.Nested(trend_follow_model), required=True, description='stock 목록'),
    'stock_info': fields.Nested(stock_info_model),
})

trend_follows_register_model = api.model('TrendFollowsRegisterModel', {
    'quant_type': fields.String(title='stock ticker'),
})

trend_follows_register_response_model = api.model('TrendFollowsRegisterModel', {
    'stock': fields.String(title='stock ticker'),
    'quant_type': fields.String(title='stock ticker'),
    'notification': fields.Boolean(title='stock ticker'),
})


@api.route('/trend_follow/<string:stock_id>', strict_slashes=False)
class Quants(Resource):

    @api.doc(params={'stock_id': 'AAPL'})
    @api.marshal_with(trend_follows_model)
    def get(self, stock_id=None):
        stock = find_stock_by_id(stock_id)
        print(stock['stock_info'])
        return { 'stock_history': stock['stock_history'] , 'stock_info': stock['stock_info']}

    @jwt_required()
    @api.expect(trend_follows_register_model)
    @api.marshal_with(trend_follows_register_response_model)
    def post(self, stock_id=None):
        requests= api.payload
        stock = register_quant_by_stock(stock_id, requests['quant_type'])
        return stock