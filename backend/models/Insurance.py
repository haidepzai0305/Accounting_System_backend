from datetime import datetime

from backend.extension import db


class Insurance(db.Model):
    __tablename__ = 'insurance'

    id = db.Column(db.Integer, primary_key=True)
    insurance_id = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # BHXH, BHYT, BHTN
    provider = db.Column(db.String(100))
    policy_number = db.Column(db.String(100))
    coverage_amount = db.Column(db.BigInteger)
    status = db.Column(db.String(20), default='active')
    effective_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    payment_method = db.Column(db.String(50))
    employee_contribution_rate = db.Column(db.Float)
    employer_contribution_rate = db.Column(db.Float)
    notes = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'insurance_id': self.insurance_id,
            'employee_id': self.employee_id,
            'type': self.type,
            'status': self.status,
            'provider': self.provider
        }