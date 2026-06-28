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
        # Optional: try to fetch the user's name
        from backend.models.User import User
        uploader = User.query.get(self.uploaded_by)
        uploader_name = uploader.full_name if uploader else "Unknown"

        return {
            'id': self.id,
            'fileId': self.file_id,
            'fileName': self.original_filename,
            'name': self.original_filename,  # alias
            'original_filename': self.original_filename,
            'fileType': self.file_type,
            'fileSize': f"{self.file_size / 1024:.2f} KB",
            'size': f"{self.file_size / 1024:.2f} KB",  # alias
            's3Key': self.s3_key,
            'relatedTable': self.related_table,
            'relatedId': self.related_id,
            'relatedRecord': f"{self.related_table}: {self.related_id}", # alias
            'uploadedBy': self.uploaded_by,
            'uploadedByName': uploader_name, # alias
            'uploadedAt': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'date': self.uploaded_at.strftime('%Y-%m-%d') if self.uploaded_at else None, # alias
            'status': 'available' # default status
        }