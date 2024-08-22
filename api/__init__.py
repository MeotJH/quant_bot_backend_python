import os
import json

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restx import Api
from werkzeug.utils import import_string

from api.common import jwt
from api.server_status import server_status_api
from api.stock import stock_api
from config import config_by_name
from util.logging_util import logger


authorizations = {
    "user_token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "JWT for user",
    },
}


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
    # sqlalchemy
    # db.init_app(app)
    # alembic
    #migrate.init_app(app, db)
    # register namespace
    api.add_namespace(server_status_api)
    api.add_namespace(stock_api)
    # register controllers
    from api.server_status import controllers
    from api.stock import controllers

    # enable CORS for front-end app
    CORS(app)

    return app
