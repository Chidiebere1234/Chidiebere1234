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
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    other_name = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    balance = db.Column(db.Float, nullable=False)
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

    def __init__(self, email, username, password):
        self.email = email
        self. username = username
        self.password = password


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

    def delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


class UserRole(db.Model):
    __tablename__ = 'user_role'
    # __table_args__ = (db.UniqueConstraint('user_id', 'role', name='unique_user_role')) Error: This has to be tuple()
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
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


    def delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


class UserImage(db.Model):
    __tablename__ = 'user_image'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('images', lazy=True))
    image_url = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class BVN(db.Model):
    __tablename__ = 'bvn'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bvn', lazy=True))
    bvn = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """ This method will save user data to database
        """
        db.session.add(self)
        db.session.commit()


    def delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()


class Bio(db.Model):
    __tablename__ = 'bios'
    id = db.Column(db.String(30), primary_key=True, default=get_uuid, nullable=False)
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


    def delete(self):
        """ This method will delete user data from database
        """
        db.session.delete(self)
        db.session.commit()
