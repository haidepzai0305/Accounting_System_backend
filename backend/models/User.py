from datetime import datetime

from backend.extension import db
from backend.enums.role_users import RoleEnum
from backend.extension.db import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(
        db.Enum(RoleEnum),
        nullable=False,
        default=RoleEnum.viewer
    )
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.full_name,
            'full_name': self.full_name,
            'role': self.role.value,
            'department': self.department,
            'phone': self.phone,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }