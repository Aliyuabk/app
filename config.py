# config.py
import os

class Config:
    SECRET_KEY = "your-secret-key"
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'pdf'}
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lessons.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
