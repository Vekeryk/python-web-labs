import os
from flask import Flask
from datetime import datetime
from flask import render_template, request, redirect, session, url_for, flash
from forms import ContactForm
from loguru import logger

app  = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
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
        receive_message(form)
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

def get_stats():
    return {
        "Operating System": os.name,
        "User agent": str(request.user_agent),
        "Current time": datetime.now().strftime("%H:%M:%S")
    }

def receive_message(form):
    logger.info(f"{form.name.data} {form.email.data} {form.phone.data} {form.subject.data} {form.message.data}")
    session['name'] = form.name.data
    session['email'] = form.email.data

if __name__ == '__main__':
    app.run(debug=True)