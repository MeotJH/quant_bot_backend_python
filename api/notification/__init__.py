from flask_restx import Namespace

notification_api = Namespace(name='notification', path='/notification', description='알림과 관련된 api 모음')