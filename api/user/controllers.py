from api import user_api as api
from flask_restx import Resource, fields
from api.user.services import save_user, find_user

email_field = fields.String(required=True, title='사용자 이메일', description="아이디로 사용됨", example='name@mail.dot',
                            pattern='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_field = fields.String(required=True, title='사용자 비밀번호', description="4자리 이상", example='password', min_length=8)
mobile_field = fields.String(required=True, title='사용자 전화번호', description='- 없음, 비번찾기 시 사용',
                             example='01012345678', pattern='^[0-9]+$', min_length=11, max_length=11)
name_field = fields.String(required=True, title='사용자 이름', description='사용자 이름', example='MeotJH')

user_request_model = api.model('UserRequestModel', {
    'userName': name_field,
    'email': email_field,
    'password': password_field,
    'mobile': mobile_field
})

user_response_model = api.model('UserResponseModel', {
    'userName': name_field,
    'email': email_field,
})

@api.route('/sign-up', strict_slashes=False)
class UserSignUp(Resource):

    @api.expect(user_request_model)
    @api.marshal_with(user_response_model)
    def post(self):
        user = api.payload
        saved_user = save_user(user=user)
        return saved_user

user_sign_in_model = api.model('UserSignInModel', {
    'email': email_field,
    'password': password_field,
})

user_sign_in_response_model = api.model('UserSignInResponseModel', {
    'email': email_field,
    'userName': name_field,
    'authorization' : fields.String(title='authorization token')
})

@api.route('/sign-in', strict_slashes=False)
class Users(Resource):

    @api.expect(user_sign_in_model)
    @api.marshal_with(user_sign_in_response_model)
    def post(self):
        user = api.payload
        saved_user = find_user(user=user)
        return saved_user