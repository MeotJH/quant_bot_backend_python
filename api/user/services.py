from api.user.model import User
from api import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from exceptions import UnauthorizedException
from flask_jwt_extended import create_access_token

def save_user(user):
    id = uuid4()
    password_hash = generate_password_hash(user['password'])
    new_user = User(uuid=id, username=user['userName'], email=user['email'], password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()

def find_user(user):
    try:
        db_user = User.query.filter_by(email=user['email']).first()
        if not check_password_hash(db_user.password, user['password']):
            raise UnauthorizedException  # 비밀번호가 틀렸을 때 예외 발생
    except UnauthorizedException:
        raise UnauthorizedException('Invalid password', 'INVALID_PASSWORD')
    response_user = db_user.to_dict()
    response_user['authorization'] = create_access_token(identity=db_user.email)

    print(response_user)
    return response_user