from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    grant = db.Column(db.String(120), nullable=False)
    month = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)