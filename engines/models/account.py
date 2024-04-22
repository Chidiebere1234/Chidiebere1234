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


class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('wallets', lazy=True))
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=2), default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def deposit(self, amount):
        pass


    def withdraw(self, amount):
        pass


    def __repr__(self):
        return f"<Account {self.account_number}>"


# Transaction History
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    transaction_id = db.Column(uuid4().hex, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_account_id = db.Column(db.String(32), db.ForeignKey('wallets.id'))
    recipient_account_id = db.Column(db.String(32), db.ForeignKey('wallets.id'))
    transaction_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('Complete', 'Declined', 'Pending', 'Under review'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __repr__(self):
        return f'<Transaction {self.id} - {self.user_id}>'
