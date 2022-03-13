from flask import Blueprint, flash, redirect, render_template, url_for, request
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


@main.route('/update_blog/<blog_id>', methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    if not blog:
        flash('Blog does not exist')
        return redirect(url_for('main.index'))

    # if changes are made, update the blog
    if request.method == 'POST':

        blog.title = request.form.get('title')
        blog.content = request.form.get('content')
        blog.category = request.form.get('category')

        db.session.commit()

        return redirect(url_for('main.index'))

    # Auto fill the blog details

    return render_template('update_blog.html', blog=blog, current_user=current_user)


@main.route('/delete_blog/<blog_id>', methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    if not blog:
        flash('Blog does not exist')
        return redirect(url_for('main.index'))

    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.index'))
