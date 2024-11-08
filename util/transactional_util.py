from contextlib import contextmanager
from api import db


@contextmanager
def transaction_scope():
    """트랜잭션 컨텍스트 매니저"""
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e