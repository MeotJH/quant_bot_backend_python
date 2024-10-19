from flask_restx import Resource
from api import notification_api as api
from api.notification.services import NotificationService



@api.route('/', strict_slashes=False)
class Notification(Resource):

    def get(self):
        NotificationService().send_notification(notification=Notification(
            title='퀀투봇 [추세추종투자]',
            body='저장했던 추세가 반전되었습니다. 지금 투자하세요',
            user_mail='name@mail.com'
        ))
        return { 'success': True }, 200