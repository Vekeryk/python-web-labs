from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app  = Flask(__name__)
app.config.from_object("config")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from app import views, models