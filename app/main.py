
import urllib
import json

from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user


from app import db
from .models import Blog, Comment


main = Blueprint('main', __name__)

# helper functions to get random quotes


def get_random_quote():
    quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(quote_url) as url:
        quote_data = url.read()
        quote = json.loads(quote_data)

        return quote


@main.route('/')
def index():
    blogs = Blog.query.all()
    quote = get_random_quote()
    return render_template('index.html', blogs=blogs, quote=quote)


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


@main.route('/blog/<blog_id>')
def blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    quote = get_random_quote()

    if not blog:
        flash('Blog does not exist')
        return redirect(url_for('main.index'))

    return render_template('blog.html', blog=blog, quote=quote)


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

    return redirect(url_for('main.blog', blog_id=blog.id))


@main.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist')
        return redirect(url_for('main.index'))

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.blog', blog_id=comment.blog_id))
