from api.notification.models import Notification
from api.user.entities import User
from exceptions import BadRequestException
from firebase_admin import messaging

class NotificationService:

    def send_notification(self, notification: Notification):
        try:
            token = self._get_user_token(notification.user_mail)
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.body,
                ),
                token=token,
            )
            print(f'this is message: {message}')
            response = messaging.send(message)
            print(f'this is response: {response}')
        except Exception as e:
            raise BadRequestException(f'{e}', 400)
        

    def _get_user_token(self, email: str) -> str:
        user = User.query.filter_by(email=email).first()
        if user:
            print(f'this is user Token: {user.app_token}')
            return user.app_token
        raise ValueError("User not found or token missing")
