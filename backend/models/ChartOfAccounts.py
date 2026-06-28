from datetime import datetime

from backend.extension import db
from backend.enums.AccountType import AccountTypeEnum


class ChartOfAccounts(db.Model):
    __tablename__ = 'chart_of_accounts'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(AccountTypeEnum, values_callable=lambda e: [x.value for x in e]), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    balance = db.Column(db.BigInteger, default=0)
    is_active = db.Column(db.Boolean, default=True)
    parent_account_code = db.Column(db.String(20), db.ForeignKey('chart_of_accounts.code'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'type': self.type.value,
            'category': self.category,
            'balance': self.balance,
            'is_active': self.is_active,
            'description': self.description,
            'parent_account_code': self.parent_account_code
        }