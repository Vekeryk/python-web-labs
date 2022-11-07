from flask import render_template, request, redirect, session, url_for, flash
from app import app, db
from app.models import Message
from app.forms import ContactForm
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
def contacts():
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