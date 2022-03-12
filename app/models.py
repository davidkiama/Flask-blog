
from enum import unique
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(), nullable=False, default='default.jpg')
