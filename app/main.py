from unicodedata import category
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_required, current_user


from app import db
from .models import Blog


main = Blueprint('main', __name__)


@main.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)


@main.route('/profile')
def profile():
    return render_template('profile.html')


@main.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        author = current_user.id

        blog = Blog(title=title, content=content,
                    category=category, author=author)

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template('create_blog.html')
