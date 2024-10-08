import logging
import os
from dotenv import load_dotenv
from constants import SingletonInstance


# JWT
class JWTConfig(SingletonInstance):
    def __init__(self):

        self.SECRET_KEY = "thisissecretkeyletmeintroducemyselfforyou"

# Flask Base Configuration
class BaseConfig(object):
    load_dotenv()
    # Flask
    ENV = "development"
    DEBUG = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = JWTConfig.instance().SECRET_KEY
    # Restx
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = False
    LOG_LEVEL = logging.DEBUG
    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f'os.getenv("SQLALCHEMY_DATABASE_URI"):{os.getenv("SQLALCHEMY_DATABASE_URI")}')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


# Flask Local Configuration
class LocalConfig(BaseConfig):
    DEBUG = True



# Flask Dev Configuration
class DevConfig(BaseConfig):
    BASE_URL = "https://localhost"


config_by_name = dict(local="config.LocalConfig", dev="config.DevConfig")
