
from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User with that username does not exist')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('Incorect password.')
            # if password is wrong, reload the page
            return redirect(url_for('auth.login'))

        # if the above check passes then...
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Lookup if email or username exists
        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()

        if user_email:
            flash('Email already exists')
            return redirect(url_for('auth.signup'))
        if user_username:
            flash('Username already taken')
            return redirect(url_for('auth.signup'))

        user = User(email=email, username=username,
                    password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))
