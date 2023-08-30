from flask import render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
from app import app, db
from app.models import UploadRecord
import datetime

uploaded_records = []  # This is a simple in-memory storage. Consider using a database for production.

@app.route('/')
def index():
    uploaded_records = UploadRecord.query.all()
    return render_template('index.html', uploaded_records=uploaded_records)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part in the request", "error")
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash("No selected file", "error")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Generate a unique filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Store the execution time and filename in the database
        record = UploadRecord(filename=unique_filename, execution_time=request.form.get('execution_time'))
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('index'))

    return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
