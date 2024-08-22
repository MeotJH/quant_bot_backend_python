from flask_restx import Namespace

stock_api = Namespace(name='stocks', path='/stocks', description='주식과 관련된 API 모음')