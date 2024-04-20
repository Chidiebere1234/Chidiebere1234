from models.model import User, db
from datetime import datetime
from uuid import uuid4


# Loan model
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.String(30), uuid4().hex, primary_key=True, nullable=False)
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


# Loan Payment model
class LoanPayment(db.Model):
    __tablename__ = 'loan_payments'
    id = db.Column(db.String(30), uuid4().hex, primary_key=True, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('loan_payments', lazy=True))
    loan_id = db.Column(db.ForeignKey('loans.id'), nullable=False)
    amount = db.Column(db.ForeignKey('loans.amount'), nullable=False) #pay attention to this
    amount_paid = db.Column(db.Float, nullable=False) # This will hold the ammount paid per day, week or month which can be deducted from the loan
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"Loan Payment id: {self.id}"


# Lender model
class Lender(db.Model):
    __tablename__ = 'lenders'
    id = db.Column(db.String(30), uuid4().hex, primary_key=True, nullable=False)
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
