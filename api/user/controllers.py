from flask_jwt_extended import get_jwt_identity, jwt_required
from api import user_api as api
from flask_restx import Resource, fields
from api.user.services import find_user_by_email, save_user, find_user, update_user_fcm_token

email_field = fields.String(required=True, title='사용자 이메일', description="아이디로 사용됨", example='name@mail.dot',
                            pattern='([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_field = fields.String(required=True, title='사용자 비밀번호', description="4자리 이상", example='password', min_length=8)
mobile_field = fields.String(required=True, title='사용자 전화번호', description='- 없음, 비번찾기 시 사용',
                             example='01012345678', pattern='^[0-9]+$', min_length=11, max_length=11)
name_field = fields.String(required=True, title='사용자 이름', description='사용자 이름', example='MeotJH')

user_sign_up_model = api.model('UserSignUpModel', {
    'userName': name_field,
    'email': email_field,
    'password': password_field,
    'mobile': mobile_field,
    'appToken': fields.String(required=True, title='앱 토큰', description='앱 토큰', example='uuid.uuid4'),
})

user_response_model = api.model('UserResponseModel', {
    'userName': name_field,
    'email': email_field,
})

@api.route('/sign-up', strict_slashes=False)
class UserSignUp(Resource):

    @api.expect(user_sign_up_model)
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


user_model = api.model('UserModel', {
    'email': email_field,
    'userName': name_field,
})


@api.route('/sign-in', strict_slashes=False)
class UsersSignIn(Resource):

    @api.expect(user_sign_in_model)
    @api.marshal_with(user_sign_in_response_model)
    def post(self):
        user = api.payload
        saved_user = find_user(user=user)
        return saved_user

user_fcm_token_model = api.model('UserFcmTokenModel', {
    'fcmToken': fields.String(required=True, title='FCM 토큰', description='FCM 토큰', example='uuid.uuid4'),
})

@api.route('/', strict_slashes=False)
class Users(Resource):
    @jwt_required()
    @api.marshal_with(user_response_model)
    def get(self):
        user = get_jwt_identity()
        find_user = find_user_by_email(user)
        return find_user
    
    @jwt_required()
    @api.expect(user_fcm_token_model)
    @api.marshal_with(fields.Boolean)
    def patch(self):
        newToken = api.payload['fcmToken']
        isUpdated = update_user_fcm_token(newToken)
        return isUpdated