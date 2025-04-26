from api.quant.model import QuantData
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields
from flask import request
from api import quant_api as api
from api.quant.services import QuantService
from api.quant.dual_momentum_services import run_dual_momentum_backtest, save_dual_momentum
from .response_models import trend_follows_model, trend_follows_register_response_model, quants_model, quant_by_user_model, quant_data_model

@api.route('/trend_follow/<string:stock_id>', strict_slashes=False)
class TrendFollow(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.quant_service = QuantService()

    @api.doc(params={'stock_id': 'AAPL'})
    @api.marshal_with(trend_follows_model)
    def get(self, stock_id=None):
        stock = self.quant_service.find_stock_by_id(stock_id)
        return { 'stock_history': stock['stock_history'] , 'stock_info': stock['stock_info']}

    @jwt_required()
    @api.expect(quant_data_model)
    @api.marshal_with(trend_follows_register_response_model)
    def post(self, stock_id):
        quant_data = QuantData(**api.payload)
        stock = self.quant_service.register_quant_by_stock(stock_id, quant_data)
        return stock
    
    @jwt_required()
    @api.marshal_with(trend_follows_register_response_model)
    def delete(self, stock_id):
        deleted_response = self.quant_service.delete_quant_by_id(stock_id)
        return deleted_response, 200
    

# 개별 거래 기록을 위한 모델
trade_record_model = api.model('TradeRecord', {
    'date': fields.DateTime,
    'best_etf': fields.String,
    '6m_return': fields.Float(allow_none=True),
    'capital': fields.Float,
    'cash_hold': fields.Float,
    'ewy_hold': fields.Float
})

# 요약 정보를 위한 모델
summary_model = api.model('Summary', {
    'initial_capital': fields.Float,
    'final_capital': fields.Float,
    'total_return': fields.Float,
    'cash_hold_return': fields.Float,
    'ewy_hold_return': fields.Float,
    'final_best_etf' : fields.String,
})

# 전체 응답을 위한 모델
backtest_response_model = api.model('BacktestResponse', {
    'data': fields.List(fields.Nested(trade_record_model)),
    'summary': fields.Nested(summary_model)
})

request_post_dual_momentum_model = api.model('SaveDualMomentumModel', {
    'type' : fields.String(title='EBITDA'),
})




@api.route('/dual_momentum', strict_slashes=False)
class DualMomentum(Resource):

    @api.doc(params={
        'etf_symbols': {'description': 'ETF 심볼 목록 (콤마로 구분 또는 다중 파라미터)', 'type': 'string', 'example': 'SPY,FEZ,EWJ'},
        'duration': {'description': '백테스트 기간 (년)', 'type': 'integer', 'default': 10},
        'savings_rate': {'description': '저축률 (%)', 'type': 'number', 'default': 3.0}
    })
    @api.marshal_with(backtest_response_model)
    def get(self):
        # 두 가지 방식 모두 처리
        etf_symbols = []
        raw_symbols = request.args.getlist('etf_symbols')
        
        for symbol in raw_symbols:
            # 콤마로 구분된 경우 분할
            etf_symbols.extend(symbol.split(','))
            
        # 빈 문자열 제거 및 중복 제거
        etf_symbols = list(filter(None, etf_symbols))
        etf_symbols = list(dict.fromkeys(etf_symbols))  # 중복 제거
        
        if not etf_symbols:
            return {'error': 'ETF symbols are required'}, 400
            
        duration = int(request.args.get('duration', 10))
        savings_rate = float(request.args.get('savings_rate', 3.0))
        
        return run_dual_momentum_backtest(etf_symbols, duration, savings_rate), 200
    
    @jwt_required()
    @api.expect(request_post_dual_momentum_model)
    @api.marshal_with(trend_follows_register_response_model)
    def post(self):
       #quant_data = QuantData(**api.payload)

        type = api.payload['type']
        return save_dual_momentum(type)

@api.route('/', strict_slashes=False)
class Quants(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.quant_service = QuantService()

    @jwt_required()
    @api.marshal_with(quants_model)
    def get(self):
        quants = self.quant_service.find_quants_by_user()
        return {'quants': quants}

@api.route('/<string:quant_id>/notification', strict_slashes=False)
class QuantNotification(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.quant_service = QuantService()

    @jwt_required()
    @api.marshal_with(quant_by_user_model)
    def patch(self, quant_id):
        quant = self.quant_service.patch_quant_by_id(quant_id)
        return quant
