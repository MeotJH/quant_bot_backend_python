from api.user.entities import User
from api import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from exceptions import UnauthorizedException
from flask_jwt_extended import create_access_token, get_jwt_identity

def save_user(user):
    id = uuid4()
    password_hash = generate_password_hash(user['password'])

    new_user = User(uuid=id,
                    username=user['userName'],
                    email=user['email'],
                    password=password_hash,
                    app_token=user.get('appToken', '')
                    )
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()

def find_user(user):
    db_user = User.query.filter_by(email=user['email']).first()
    if not check_password_hash(db_user.password, user['password']):
        raise UnauthorizedException('Invalid password', 'INVALID_PASSWORD')  # 비밀번호가 틀렸을 때 예외 발생
    response_user = db_user.to_dict()
    response_user['authorization'] = create_access_token(identity=db_user.email)
    return response_user

def find_user_by_email(email):
    db_user = User.query.filter_by(email=email).first()
    return db_user.to_dict()

def update_user_fcm_token(newToken):
    email = get_jwt_identity()
    db_user = User.query.filter_by(email=email).first()
    db_user.app_token = newToken
    db.session.commit()
    return True