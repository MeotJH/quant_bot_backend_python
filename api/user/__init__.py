from flask_restx import Namespace

user_api = Namespace(name='users', path='/users', description='유저와 관련된 API 모음')