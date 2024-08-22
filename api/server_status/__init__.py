from flask_restx import Namespace

server_status_api = Namespace(
    name='status',
    path='/status',
    description='서비스 상태 확인 관련 API 모음',
)