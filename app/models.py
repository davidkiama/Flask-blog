
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.String(), nullable=False, default='default.svg')
    blogs = db.relationship('Blog', backref='user', passive_deletes=True)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(5000))
    category = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, default=db.func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)

    comments = db.relationship(
        'Comment', backref='blog', passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, default=db.func.now())

    blog_id = db.Column(db.Integer, db.ForeignKey(
        'blog.id', ondelete='CASCADE'), nullable=False)
