from flask import render_template, request, redirect, url_for
from datetime import datetime
import os
from . import home_bp

@home_bp.route('/')
def index():
    return render_template("home.html", stats=get_stats())

@home_bp.route("/about")
def about():
    return render_template("about.html", stats=get_stats())

@home_bp.route("/social")
def social():
    return render_template("social.html", stats=get_stats())

@home_bp.route("/portfolio")
def portfolio():
    return redirect(url_for("home.index"))

def get_stats():
    return {
        "Operating System": os.name,
        "User agent": str(request.user_agent),
        "Current time": datetime.now().strftime("%H:%M:%S")
    }
