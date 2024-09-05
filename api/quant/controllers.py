from flask_restx import fields, Resource

from api import quant_api as api
from api.quant.services import find_stock_by_id

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

trend_follows_model = api.model('TrendFollowsModel', {
    'trend_follows': fields.List(fields.Nested(trend_follow_model), required=True, description='stock 목록'),
})


@api.route('/trend_follow/<string:stock_id>', strict_slashes=False)
class Stocks(Resource):

    @api.doc(params={'stock_id': 'AAPL'})
    @api.marshal_with(trend_follows_model)
    def get(self, stock_id=None):
        stock = find_stock_by_id(stock_id)
        return { 'trend_follows': stock }