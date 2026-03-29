from datetime import datetime

from backend.extension import db
from backend.enums.TransactionStatus import TransactionStatusEnum
from backend.utils.transaction_status_type import TransactionStatusType


class CashOutDetail(db.Model):
    __tablename__ = 'cash_out_detail'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    currency = db.Column(db.String(3), default='VND')
    category = db.Column(db.String(100), nullable=False)  # Lương, Bảo trì, Mua sắm
    description = db.Column(db.String(500), nullable=False)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'))
    account_debit = db.Column(db.String(20), db.ForeignKey('chart_of_accounts.code'), nullable=False)
    account_credit = db.Column(db.String(20), db.ForeignKey('chart_of_accounts.code'), nullable=False)
    status = db.Column(
        TransactionStatusType(),
        nullable=False,
        default=TransactionStatusEnum.PENDING,
    )
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.String(500))
    notes = db.Column(db.String(500))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'date': self.date.isoformat(),
            'amount': self.amount,
            'currency': self.currency,
            'category': self.category,
            'description': self.description,
            'account_debit': self.account_debit,
            'account_credit': self.account_credit,
            'status': self.status.value,
            'created_at': self.created_at.isoformat()
        }