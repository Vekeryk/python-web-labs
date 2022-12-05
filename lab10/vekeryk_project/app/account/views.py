from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

from .. import db
from .models import User
from .forms import RegistrationForm, LoginForm
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


@account_bp.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", category='success')
    return redirect(url_for("account.login"))


@account_bp.route('/account')
@login_required
def account_profile():
    return render_template('account.html')


@account_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
