from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from uuid import uuid4


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


def get_uuid():
    return uuid4().hex

# User model for authentication
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    other_name = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(128), unique=True, nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    balance = db.Column(db.Float, default='0.0')
    loan_active = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    staff = db.Column(db.Boolean, default=False)
    superuser = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)
    suspended = db.Column(db.Boolean, default=False)
    online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """ User Class Model Representation

        return: user's username
        """
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


class UserRole(db.Model):
    __tablename__ = 'user_role'
    # __table_args__ = (db.UniqueConstraint('user_id', 'role', name='unique_user_role')) Error: This has to be tuple()
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('roles', lazy=True))
    role = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


class UserImage(db.Model):
    __tablename__ = 'user_image'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('images', lazy=True))
    image_url = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# BVN Model 
class BVN(db.Model):
    __tablename__ = 'bvn'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bvn', lazy=True))
    bvn = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Bio Model
class Bio(db.Model):
    __tablename__ = 'bios'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bios', lazy=True))
    fingerprint = db.Column(db.String(300), nullable=True)
    live_picture = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Wallet Model
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
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


    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Transaction History
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    transaction_id = db.Column(db.String(32), default=get_uuid, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_account_id = db.Column(db.String(32), db.ForeignKey('wallets.id'))
    recipient_account_id = db.Column(db.String(32), db.ForeignKey('wallets.id'))
    transaction_type = db.Column(db.String(128), nullable=True)
    description = db.Column(db.String(950), nullable=True)
    status = db.Column(db.Enum('Complete', 'Declined', 'Pending', 'Under review'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __repr__(self):
        return f'<Transaction {self.id} - {self.user_id}>'


    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Loan model
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False) # Adjust later
    rate = db.Column(db.Float, nullable=False) # Adjust later
    approved = db.Column(db.Boolean, default=False)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Loan by: {self.borrower.first_name}>'


    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Loan Payment model
class LoanPayment(db.Model):
    __tablename__ = 'loan_payments'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('loan_payments', lazy=True))
    loan_id = db.Column(db.String(32), nullable=False)
    amount = db.Column(db.String(32), nullable=False) #pay attention to this
    amount_paid = db.Column(db.Float, nullable=False) # This will hold the ammount paid per day, week or month which can be deducted from the loan
    weekly_payment = db.Column(db.Boolean, default=False)
    monthly_payment = db.Column(db.Boolean, default=False)
    last_payment = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"Loan Payment id: {self.id}"

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Lender model
class Lender(db.Model):
    __tablename__ = 'lenders'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('lenders', lazy=True))
    name = db.Column(db.String(80), nullable=False)
    available_funds = db.Column(db.Float, nullable=False)
    preferred_rate = db.Column(db.Float, nullable=False)
    max_loan_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Lender {self.id} - {self.name}>'

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Notification model
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    allow_transaction_notifications = db.Column(db.Boolean, default=True)
    allow_dispute_notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


# Dispute model
class Dispute(db.Model):
    __tablename__ = 'disputes'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('disputes', lazy=True))
    category = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Dispute {self.id}>'

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ This method will commit any new updates when called
        """
        db.session.commit()

    def _delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()
