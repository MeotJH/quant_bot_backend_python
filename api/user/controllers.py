from api import user_api as api
from flask_restx import Resource, fields
from api.user.services import save_user


user_request_model = api.model('UserRequestModel', {
    'userName': fields.String(title='stock ticker'),
    'email': fields.String(title='stock name'),
    'password': fields.String(title='stock price'),
})

user_response_model = api.model('UserResponseModel', {
    'userName': fields.String(title='stock ticker'),
    'email': fields.String(title='stock name'),
})

@api.route('/', strict_slashes=False)
class Users(Resource):

    @api.expect(user_request_model)
    @api.marshal_with(user_response_model)
    def post(self):
        user = api.payload
        saved_user = save_user(user=user)
        return saved_user