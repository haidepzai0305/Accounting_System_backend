from datetime import datetime

from backend.extension import db


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    identification_number = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    basic_salary = db.Column(db.BigInteger, nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, retired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.full_name,
            'full_name': self.full_name,
            'fullName': self.full_name,
            'department': self.department,
            'position': self.position,
            'basic_salary': self.basic_salary,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'username': self.employee_id,
            'role': 'viewer'
        }