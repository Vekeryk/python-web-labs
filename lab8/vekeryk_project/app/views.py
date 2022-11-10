from urllib.parse import urljoin, urlparse
from flask import render_template, request, redirect, session, url_for, flash, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import Message, User
from app.forms import ContactForm, LoginForm, RegistrationForm
from datetime import datetime
from loguru import logger
import os

logger.add("messages.log")

@app.route('/')
def index():
    return render_template("home.html", stats=get_stats())

@app.route("/about")
def about():
    return render_template("about.html", stats=get_stats())

@app.route("/social")
def social():
    return render_template("social.html", stats=get_stats())

@app.route("/portfolio")
def portfolio():
    return redirect(url_for("index"))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        save_message(form)
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category = 'warning')
        return render_template('contact.html', form=form)

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', form=form)

@app.route('/clear')
def clear():
    session.pop("email", default=None)
    session.pop("name", default=None)
    return redirect(url_for("contact"))

@app.route('/messages')
@login_required
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@app.route('/messages/delete/<id>')
def delete_message(id):
    Message.query.filter_by(id=id).delete()
    try:
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("messages"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Account created for {form.username.data}!", category='success')
            return redirect(url_for("login"))
        except:
            db.session.flush()
            db.session.rollback()

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You have been logged in", category='success')
            next = request.args.get('next')
            print(next)
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('account'))
        else:
            flash(f"Email or password is incorrect", category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out", category='success')
    return redirect(url_for("login"))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_stats():
    return {
        "Operating System": os.name,
        "User agent": str(request.user_agent),
        "Current time": datetime.now().strftime("%H:%M:%S")
    }

def save_message(form):
    subject = dict(form.subject.choices).get(form.subject.data)
    logger.info(f"{form.name.data} {form.email.data} {form.phone.data} {subject} {form.message.data}")
    session['name'] = form.name.data
    session['email'] = form.email.data
    message = Message(
        name = form.name.data,
        email = form.email.data,
        phone = form.phone.data,
        subject = subject,
        message = form.message.data
    )
    try:
        db.session.add(message)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True)