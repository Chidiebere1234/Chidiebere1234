from models.model import User, db
from datetime import datetime
from uuid import uuid4


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.String(30), uuid4().hex, primary_key=True, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    allow_transaction_notifications = db.Column(db.Boolean, default=True)
    allow_dispute_notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
