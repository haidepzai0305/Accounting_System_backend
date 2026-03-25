from datetime import datetime

from backend.extension import db


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(50), unique=True, nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    s3_key = db.Column(db.String(500))
    transaction_id = db.Column(db.String(50), db.ForeignKey('cash_in_detail.transaction_id'))
    related_table = db.Column(db.String(50))
    related_id = db.Column(db.String(50))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'file_id': self.file_id,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size
        }