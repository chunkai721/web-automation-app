from datetime import datetime
from app import db

class UploadRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    execution_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String(120), default='Pending')
