from datetime import datetime
from app import db

class UploadRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    execution_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String(120), default='Pending')
    notes = db.Column(db.String(500))  # 增加備註欄位
    completed = db.Column(db.Boolean, default=False)  # Indicates if the task is completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when the record was created
