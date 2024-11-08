from api.quant.model import QuantData
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from api import quant_api as api
from api.quant.services import QuantService

from .response_models import trend_follows_model, trend_follows_register_response_model, quants_model, quant_by_user_model, quant_data_model

@api.route('/trend_follow/<string:stock_id>', strict_slashes=False)
class Quant(Resource):
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
