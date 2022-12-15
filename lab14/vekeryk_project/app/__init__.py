from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
ckeditor = CKEditor()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.todo import todo_bp
        from app.feedback import feedback_bp
        from app.account import account_bp
        from app.category_api import category_api_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(feedback_bp, url_prefix='/feedback')
        app.register_blueprint(account_bp)
        app.register_blueprint(todo_bp)
        app.register_blueprint(category_api_bp, url_prefix='/api')

    return app
