from datetime import datetime

from backend.extension import db


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # income_statement, balance_sheet, cash_flow
    period = db.Column(db.String(10))  # YYYY-MM
    title = db.Column(db.String(200), nullable=False)
    data = db.Column(db.JSON)  # JSON data
    summary = db.Column(db.JSON)
    status = db.Column(db.String(20), default='draft')  # draft, generated, published, archived
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    generated_at = db.Column(db.DateTime)
    published_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    published_at = db.Column(db.DateTime)
    file_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'type': self.type,
            'period': self.period,
            'title': self.title,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }