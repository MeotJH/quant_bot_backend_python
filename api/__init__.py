import os
import json

from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from werkzeug.utils import import_string
from flask_jwt_extended import JWTManager

from api.common import jwt
from api.server_status import server_status_api
from api.stock import stock_api
from api.quant import quant_api
from api.user import user_api
from api.notification import notification_api
from config import config_by_name
from util.logging_util import logger

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

authorizations = {
    "user_token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT for user",
    },
}
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # for zappa health check;
    app.add_url_rule("/", endpoint="ping", view_func=lambda: "Pong!")

    # app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(
        app,
        authorizations=authorizations,
        security="user_token",
        doc="/swagger",
        title="template-flask",
        version="1.0",
        description="Flask-Restx를 이용한 백엔드 API",
        prefix='/api/v1',
    )
    
    config_name = os.getenv("TEMP_FLASK_ENV", "local")
    print(f"config_env:{config_name}")
    config_object = import_string(config_by_name[config_name])()
    app.config.from_object(config_object)


    # 참조하는 모든 라이브러리의 로그 레벨을 변경하고 싶을때 아래 코드를 주석 풀면 모든 라이브러리의 로그가 출력된다.
    # logger.set_level(None, app.config['LOG_LEVEL'])

    # 텝플릿 에서 사용하는 기본 logger 설정
    logger.set_default_logger_level(app.name, app.config["LOG_LEVEL"])

    # dynamodb logger 설정
    logger.set_level(logger_name="pynamodb", level=app.config["LOG_LEVEL"])

    # firebase admin 설정

    # jwt
    jwt.init_app(app)
    # register namespace
    api.add_namespace(server_status_api)
    api.add_namespace(stock_api)
    api.add_namespace(quant_api)
    api.add_namespace(user_api)
    api.add_namespace(notification_api)
    # register controllers
    from api.server_status import controllers
    from api.stock import controllers
    from api.quant import controllers
    from api.user import controllers
    from api.notification import controllers

    # enable CORS for front-end app
    CORS(app)
    # sqlalchemy 및 데이터베이스 DDL 관리 lib 
    #db.init_app(app)
    #migrate.init_app(app, db)

    from api.quant.entities import Quant
    from api.user.entities import User

    from api.quant.scheduler import QuantScheduler
    quant_scheduler = QuantScheduler(app)  # app 인스턴스를 전달

    with app.app_context():
        # 데이터베이스 초기화
        db.init_app(app)
        migrate.init_app(app, db)

        # 스케줄러 시작
        quant_scheduler.start()

    import atexit
    atexit.register(quant_scheduler.shutdown)

    return app
