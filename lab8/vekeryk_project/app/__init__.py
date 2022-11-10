from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app  = Flask(__name__)
app.config.from_object("config")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from app import views, models