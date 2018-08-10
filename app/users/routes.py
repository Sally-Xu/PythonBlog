from app import db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
    ResetRequestForm, ResetPasswordForm)

from models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime

from users.util import save_picture, send_request_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if(form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created, You are now able to login!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form = form, title='Register')

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter(User.email.ilike(form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccesful, please try again', 'danger')

    return render_template('login.html', form = form, title='Login')

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.image_file = image_file

        current_user.username=form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title = 'Account', form = form, image_file = image_file)
        
@users.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if (current_user.is_authenticated):
        return redirect(url_for('main.home'))

    form = ResetRequestForm()
    if form.validate_on_submit():   
        user = User.query.filter(User.email.ilike(form.email.data)).first()
        send_request_email(user)
        flash('An email with instructions to reset your password has been sent to you, please check your email')
        return redirect(url_for('users.reset_request'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):

    if (current_user.is_authenticated):
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset, You are now able to login!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)

@users.route("/")
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # order = request.args.get('order', desc, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page = 5, page = page)
    return render_template('user_posts.html', posts = posts, user=user)