from flask import render_template, session, flash, redirect, url_for, request
from flask_login import login_required
from .. import db
from .models import Message
from .forms import ContactForm

from . import feedback_bp


@feedback_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        save_message(form)
        flash(
            f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("feedback.contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category='warning')
        return render_template('contact.html', form=form)

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', form=form)


@feedback_bp.route('/messages')
@login_required
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)


@feedback_bp.route('/messages/delete/<id>')
@login_required
def delete_message(id):
    message = Message.query.get_or_404(id)
    try:
        db.session.delete(message)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("feedback.messages"))


def save_message(form):
    subject = dict(form.subject.choices).get(form.subject.data)
    session['name'] = form.name.data
    session['email'] = form.email.data
    message = Message(
        name=form.name.data,
        email=form.email.data,
        phone=form.phone.data,
        subject=subject,
        message=form.message.data
    )
    try:
        db.session.add(message)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
