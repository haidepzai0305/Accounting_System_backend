from datetime import datetime

from backend.extension import db


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    journal_id = db.Column(db.String(50), unique=True, nullable=False)
    transaction_id = db.Column(db.String(50))
    period = db.Column(db.String(10))  # YYYY-MM
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    account_debit = db.Column(db.String(20), db.ForeignKey('chart_of_accounts.code'), nullable=False)
    account_credit = db.Column(db.String(20), db.ForeignKey('chart_of_accounts.code'), nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, posted, reversed
    is_system_generated = db.Column(db.Boolean, default=True)
    reference_id = db.Column(db.Integer)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_at = db.Column(db.DateTime)
    notes = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'journal_id': self.journal_id,
            'date': self.date.isoformat(),
            'description': self.description,
            'account_debit': self.account_debit,
            'account_credit': self.account_credit,
            'amount': self.amount,
            'status': self.status
        }