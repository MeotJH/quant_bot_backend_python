from api.user.model import User
from api import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

def save_user(user):
    id = uuid4()
    password_hash = generate_password_hash(user['password'])
    new_user = User(uuid=id, username=user['userName'], email=user['email'], password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return new_user