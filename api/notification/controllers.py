from flask_restx import Resource, fields
from flask import request, jsonify
import json
from api import notification_api as api
from api.notification.services import NotificationService
from pywebpush import webpush, WebPushException

subscriptions = []

@api.route('/', strict_slashes=False)
class Notification(Resource):

    def get(self):
        NotificationService().send_notification(notification=Notification(
            title='퀀투봇 [추세추종투자]',
            body='저장했던 추세가 반전되었습니다. 지금 투자하세요',
            user_mail='name@mail.com'
        ))
        return { 'success': True }, 200


subscription_model = api.model("Subscription", {
    "endpoint": fields.String(required=True, description="푸시 서버 엔드포인트"),
    "keys": fields.Nested(api.model("Keys", {
        "p256dh": fields.String(required=True, description="Public Key"),
        "auth": fields.String(required=True, description="Auth Key")
    }))
})


@api.route('/subscribe', strict_slashes=False)
class NotificationSub(Resource):

    @api.expect(subscription_model)
    def post(self):
        """ 🔹 웹 푸시 구독 저장 """
        

        """
        알림처리 로그인 되어있어야 알림받을 수 있다.
        알림 처리 할때 유저스토리
        하나도 값 없다 첫 퀀트받기 클릭 -> 푸시 구독 저장
        알림off -> 푸시 정보 삭제
        알림on -> 푸시 구독 저장

        db구조 유저 id 기준으로 -> uuid str / 유저 str / 구독 데이터 json
        1유저당 1알림
        """
        subscription_json = request.get_json()
        subscriptions.append(subscription_json)  # 구독 정보 저장
        print("✅ 저장된 구독 정보:", subscription_json)
        return {"success": True, "message": "구독 성공"}, 201


import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

@api.route('/send', strict_slashes=False)
class NotificationSend(Resource):

    #@api.expect(subscription_model)
    def get(self):
        """ 🔹 웹 푸시 구독 저장 """

        payload = {
            "title": "제목입니다.",
            "body": "바디입니다.",
            "url": "https://quantwo-bot.com"
        }
        private_key_pem = convert_vapid_private_key_to_pem("LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JR0hBZ0VBTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEJHMHdhd0lCQVFRZ3RWUUYrZXBmcEdkTFh6MEIKcEUvRzl6UEZ2VVdTTkh1Y2JHVXY5anJtaEJpaFJBTkNBQVMwaEZNUTJVc2U1RXJIN29oV0lrWWcrclNXQlhkNgpuR2VUcUc3STZVdmtQcnJHOGh3V0EwUGVOSjdmQTNQVTEzOTlTdU1ZaHRyYVdsU0dyOUp2K1VFUAotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg==")
        private_key_pem_str = private_key_pem.decode("utf-8")
        print(f":::::::::::: this is perm str ::::::::>>>>>>>> {private_key_pem_str}")
        for sub in subscriptions:
            try:
                webpush(
                    subscription_info=sub,
                    data=json.dumps(payload),
                    vapid_private_key= "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgtqmO6plI6Ftq6FqOudWqPR0pbDu6eZIotEyV_i5GiwOhRANCAASJR4DrPoM9bg5vhVlFOkTRy0fKJ677hrZYKFAeAX0LoRCedb5AD5tZwU8umWZ_Pn6hEp0BWwcz9AF4JAemx7kb",
                    vapid_claims={
                            "sub": "mailto:mallangyi@naver.com"  # 관리자 이메일
                        },
                )
                print("✅ 푸시 성공:", sub["endpoint"])
            except WebPushException as e:
                print(f"❌ 푸시 전송 실패: {e}")
                if e.response:
                    print("🔴 응답 상태 코드:", e.response.status_code)
                    print("🔴 응답 본문:", e.response.text)

        return {"success": True, "message": "푸시 알림 전송 완료"}, 200

def convert_vapid_private_key_to_pem(private_key_str: str) -> bytes:
    """
    private_key_str 은 이미 '-----BEGIN PRIVATE KEY----- ...' 형태의 PEM을
    Base64로 감싼 문자열이므로, Base64 디코딩 후 load_pem_private_key 로 로드하면 된다.
    """
    pem_data = base64.urlsafe_b64decode(private_key_str)
    # 이 부분에서 곧바로 불필요한 PEM 재-인코딩 없이 써도 되지만
    # 필요하면 실제 key 객체로 파싱한 다음에 다시 bytes 로도 변환할 수 있음
    return pem_data