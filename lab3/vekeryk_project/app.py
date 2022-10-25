import os
from flask import Flask
from datetime import datetime
from flask import render_template, request, redirect, url_for

app  = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html", stats=get_stats())

@app.route("/about")
def about():
    return render_template("about.html", stats=get_stats())

@app.route("/contacts")
def contacts():
    return render_template("contacts.html", stats=get_stats())

@app.route("/portfolio")
def portfolio():
    return redirect(url_for("index"))

def get_stats():
    return {
        "Operating System": os.name,
        "User agent": str(request.user_agent),
        "Current time": datetime.now().strftime("%H:%M:%S")
    }

if __name__ == '__main__':
    app.run(debug=True)