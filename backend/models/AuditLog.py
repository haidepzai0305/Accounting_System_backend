from datetime import datetime

from backend.extension import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, approve, reject
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.String(50))
    old_value = db.Column(db.JSON)
    new_value = db.Column(db.JSON)
    change_summary = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    status_code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'log_id': self.log_id,
            'user_id': self.user_id,
            'action': self.action,
            'table_name': self.table_name,
            'timestamp': self.timestamp.isoformat()
        }
