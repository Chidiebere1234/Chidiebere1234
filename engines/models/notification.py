from models.model import db, User
from datetime import datetime
from uuid import uuid4


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
