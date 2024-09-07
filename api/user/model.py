# myapp/models.py
import uuid
from api import db
from sqlalchemy.dialects.postgresql import UUID

# 모델 정의
class User(db.Model):
    #id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userName': self.username,  # username을 userName으로 변경하여 반환
            'email': self.email
        }