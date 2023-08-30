import os

# Determine the absolute path of the application's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuration for the web application
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}

# Scheduler Configuration
SCHEDULER_API_ENABLED = True

# Use the absolute path to specify the location of the SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
