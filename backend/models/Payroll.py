from datetime import datetime

from backend.extension import db
from backend.enums.PayrollStatus import PayrollStatusEnum


class Payroll(db.Model):
    __tablename__ = 'payroll'

    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.String(50), unique=True, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    basic_salary = db.Column(db.BigInteger, nullable=False)
    allowance = db.Column(db.BigInteger, default=0)
    bhxh_rate = db.Column(db.Float, default=0.08)
    bhxh_amount = db.Column(db.BigInteger, default=0)
    bhyt_rate = db.Column(db.Float, default=0.015)
    bhyt_amount = db.Column(db.BigInteger, default=0)
    tax_rate = db.Column(db.Float, default=0.05)
    tax_amount = db.Column(db.BigInteger, default=0)
    deductions = db.Column(db.BigInteger, default=0)
    status = db.Column(db.Enum(PayrollStatusEnum, values_callable=lambda e: [x.value for x in e]), default=PayrollStatusEnum.DRAFT)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    payment_date = db.Column(db.Date)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid_at = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(50), db.ForeignKey('cash_out_detail.transaction_id'))
    notes = db.Column(db.String(500))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def brutto_salary(self):
        return self.basic_salary + self.allowance

    @property
    def total_deductions(self):
        return self.bhxh_amount + self.bhyt_amount + self.tax_amount + self.deductions

    @property
    def netto_salary(self):
        return self.brutto_salary - self.total_deductions

    def calculate_payroll(self):
        self.bhxh_amount = int(self.basic_salary * self.bhxh_rate)
        self.bhyt_amount = int(self.basic_salary * self.bhyt_rate)
        self.tax_amount = int(self.brutto_salary * self.tax_rate)

    def to_dict(self):
        return {
            'id': self.id,
            'payroll_id': self.payroll_id,
            'month': self.month,
            'year': self.year,
            'employee_id': self.employee_id,
            'basic_salary': self.basic_salary,
            'allowance': self.allowance,
            'brutto_salary': self.brutto_salary,
            'bhxh_amount': self.bhxh_amount,
            'bhyt_amount': self.bhyt_amount,
            'tax_amount': self.tax_amount,
            'total_deductions': self.total_deductions,
            'netto_salary': self.netto_salary,
            'status': self.status.value,
            'created_at': self.created_at.isoformat()
        }