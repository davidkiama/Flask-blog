
from crypt import methods
from unicodedata import name
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user


from app import db
from .models import Blog, Comment


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


# Helper functoion to check if blog exists


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


@main.route('/blog/<blog_id>')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    if not blog:
        flash('Blog does not exist')
        return redirect(url_for('main.index'))

    return render_template('blog.html', blog=blog)


@main.route('/create-comment/<blog_id>', methods=['GET', 'POST'])
def create_comment(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    if not blog:
        flash('Blog does not exist')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('name')
        comment = request.form.get('comment')

        comment = Comment(name=username, content=comment, blog_id=blog.id)

        db.session.add(comment)
        db.session.commit()

    return render_template('blog.html', blog=blog)
