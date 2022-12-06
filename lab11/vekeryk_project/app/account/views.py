import os
import secrets
from PIL import Image, ImageOps
from flask import current_app, render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql.functions import now
from urllib.parse import urlparse, urljoin

from .. import db
from .models import User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from . import account_bp


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash(
                f"Account created for {form.username.data}!", category='success')
            return redirect(url_for("account.login"))
        except:
            db.session.flush()
            db.session.rollback()

    return render_template('register.html', form=form)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in", category='success')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('account.account_profile'))
        else:
            flash(f"Email or password is incorrect", category='danger')
    return render_template('login.html', form=form)


@account_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
        flash(f"Password successfully changed", category='success')
        return redirect(url_for('account.account_profile'))
    return render_template('reset_password.html', form=form)

@account_bp.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", category='success')
    return redirect(url_for("account.login"))


@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account_profile():
    print(current_user.last_seen)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@account_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@account_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extention = os.path.splitext(form_picture.filename)
    picture_name = random_hex + file_extention
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_name)

    output_size = (125, 125)
    image = Image.open(form_picture)
    thumb = ImageOps.fit(image, output_size, Image.ANTIALIAS)
    thumb.save(picture_path)

    return picture_name