from contextlib import contextmanager

from flask_jwt_extended import JWTManager
#from flask_migrate import Migrate
#from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()

#db = SQLAlchemy()

#migrate = Migrate()


@contextmanager
def transact():
    try:
        yield
        #db.session.commit()
    except Exception:
        #db.session.rollback()
        raise


#transactional = transact()
