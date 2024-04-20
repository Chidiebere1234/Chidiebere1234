from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from .model import User
from uuid import uuid4


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


def get_uuid():
    return uuid4().hex


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    allow_transaction_notifications = db.Column(db.Boolean, default=True)
    allow_dispute_notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
