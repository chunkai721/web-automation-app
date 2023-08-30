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
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    # Order by 'completed' in ascending order (incomplete tasks first), 
    # then by 'created_at' in descending order (newest tasks first).
    uploaded_records = UploadRecord.query.order_by(UploadRecord.completed, UploadRecord.created_at.desc()).all()
    
    return render_template('index.html', uploaded_records=uploaded_records, current_time=current_time)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part in the request", "error")
        return redirect(url_for('index'))

    file = request.files['file']
    execution_time = request.form.get('execution_time')
    notes = request.form.get('notes')  # Get the notes from the form

    # Check if the necessary fields are filled
    if not file or not execution_time:
        flash("所有欄位都必須填寫！", "error")
        return redirect(url_for('index'))

    if file.filename == '':
        flash("No selected file", "error")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Generate a unique filename
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Convert execution_time from string to datetime object
        execution_time_str = request.form.get('execution_time')
        execution_time_obj = datetime.datetime.strptime(execution_time_str, '%Y-%m-%dT%H:%M')

        # Store the execution time, filename, and notes in the database
        record = UploadRecord(filename=unique_filename, execution_time=execution_time_obj, notes=notes)  # Add notes here
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('index'))

    return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/redo/<int:record_id>', methods=['POST'])
def redo_upload(record_id):
    original_record = UploadRecord.query.get_or_404(record_id)
    
    # Convert execution_time from string to datetime object
    execution_time_str = request.json['execution_time']
    execution_time_obj = datetime.datetime.strptime(execution_time_str, '%Y-%m-%dT%H:%M')

    # Create a new record with the same filename and new execution time
    new_record = UploadRecord(
        filename=original_record.filename,
        notes=original_record.notes,  # Copy the notes from the original record
        execution_time=execution_time_obj
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Success"}), 200

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_upload(record_id):
    record = UploadRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/mark_completed/<int:record_id>', methods=['POST'])
def mark_completed(record_id):
    record = UploadRecord.query.get_or_404(record_id)
    record.completed = True
    db.session.commit()
    return redirect(url_for('index'))