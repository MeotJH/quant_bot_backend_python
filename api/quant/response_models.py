from api import quant_api as api
from flask_restx import fields, Resource

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

quant_by_user_model = api.model('QuantByUserModel', {
    'id': fields.String(title='id'),
    'ticker': fields.String(title='stock'),
    'name' : fields.String(title='stock name'),
    'quant_type': fields.String(title='stock quant_type'),
    'notification': fields.Boolean(title='notification'),
    'profit' : fields.String(title='profit'),
    'profit_percent' : fields.String(title='profit_percent'),
    'initial_status': fields.String(required=True, description='초기 상태 (높음/낮음)'),
    'current_status': fields.String(required=True, description='현재 상태 (높음/낮음)')
})

quants_model = api.model('QuantsModel', {
    'quants': fields.List(fields.Nested(quant_by_user_model), description='List of quants models')
})

quant_data_model = api.model('QuantDataModel', {
    'stock': fields.String(required=True, description='주식 코드'),
    'quant_type': fields.String(required=True, description='퀀트 투자 유형'),
    'initial_price': fields.Float(required=True, description='초기 주가'),
    'initial_trend_follow': fields.Float(required=True, description='초기 이동평균선 값'),
    'initial_status': fields.String(required=True, description='초기 상태 (높음/낮음)')
})