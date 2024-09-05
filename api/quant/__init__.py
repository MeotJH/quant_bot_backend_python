from flask_restx import Namespace

quant_api = Namespace(name='quants', path='/quants', description='주식 퀀트 투자 방법과 관련된 API 모음')