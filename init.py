from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from sqlalchemy import inspect
import sqlite3

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



import logging
logging.basicConfig()

# Initialize Flask app
app = Flask(__name__)

# Ensure the 'data' directory exists for the SQLite database
os.makedirs('data', exist_ok=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath('data'), 'users.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save uploaded files
app.config['SECRET_KEY'] = 'your_secret_key_here'  # For session management


for folder in [app.config['UPLOAD_FOLDER'], 'static/plots', 'static/reports']:
    os.makedirs(folder, exist_ok=True)

# Create necessary folders if they do not exist
for folder in [app.config['UPLOAD_FOLDER'], 'static/plots', 'static/reports']:
    os.makedirs(folder, exist_ok=True)

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'