# myapp/entityies.py
import uuid
from api import db
from sqlalchemy.dialects.postgresql import UUID


# 모델 정의
class Quant(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stock = db.Column(db.String(40), unique=False, nullable=False)
    notification = db.Column(db.Boolean, unique=False, nullable=False)
    quant_type = db.Column(db.String(30), unique=False, nullable=False)


    initial_price = db.Column(db.Float, unique=False, nullable=False)
    initial_trend_follow = db.Column(db.Float, unique=False, nullable=False)
    # 처음 저장한 상태
    initial_status = db.Column(db.String(10), unique=False, nullable=False)
    # 현재 상태 notification 을 보내기 위해서 계속 바뀌는 값
    current_status = db.Column(db.String(10), unique=False, nullable=False)

    # user의 uuid를 외래 키로 가져옴
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uuid'), nullable=False)

    def __repr__(self):
        return f'<Quant {self.stock}>'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'stock': self.stock,
            'notification': self.notification,
            'user_id': self.user_id,
            'quant_type': self.quant_type
        }