from flask import Flask
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, SCHEDULER_API_ENABLED, SQLALCHEMY_DATABASE_URI
import secrets
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 生成一個32字符長的隨機hex token
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['SCHEDULER_API_ENABLED'] = SCHEDULER_API_ENABLED
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 通常建議將此設置為False以避免額外的記憶體開銷

db = SQLAlchemy(app)

from app import routes, models
