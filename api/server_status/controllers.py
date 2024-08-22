from http import HTTPStatus

from flask_restx import Resource

from api import server_status_api as api


@api.route('/health-check', strict_slashes=False)
class HealthCheck(Resource):
    @api.doc(security=None, description='헬스 체크 API')
    @api.response(code=HTTPStatus.OK.value, description='서버가 정상적으로 구동 되고 있음')
    def get(self) -> HTTPStatus:
        return HTTPStatus.OK
