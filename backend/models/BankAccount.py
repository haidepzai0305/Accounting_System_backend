from datetime import datetime

from backend.extension import db


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), unique=True, nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.BigInteger, default=0)
    currency = db.Column(db.String(3), default='VND')
    account_type = db.Column(db.String(50))  # checking, savings
    status = db.Column(db.String(20), default='active')
    last_reconciled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'bank_name': self.bank_name,
            'account_number': self.account_number,
            'account_holder': self.account_holder,
            'balance': self.balance,
            'currency': self.currency,
            'status': self.status
        }