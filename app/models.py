from . import db
import time


def _get_date():
    return time.time()


class BaseModel(object):
    created_at = db.Column(db.Integer, default=_get_date)
    updated_at = db.Column(db.Integer, default=_get_date)


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    pwd = db.Column(db.String(64), nullable=False)


class File(BaseModel, db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
