from . import bcrypt
from . import db, login_manager
from flask_login import UserMixin

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=True)
    email = db.Column(db.String(40), unique=False, nullable=True)
    phone = db.Column(db.String(15), unique=False, nullable=True)
    subject = db.Column(db.Integer, unique=False, nullable=True)
    message = db.Column(db.Text, unique=False, nullable=True)
   
    def repr(self):
        return f"""Message('{self.message}', '{self.email}')"""

        
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password_hashed = db.Column(db.String(40), unique=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('Is not readable')

    @password.setter
    def password(self, password):
        print("setter method called")
        self.password_hashed = bcrypt.generate_password_hash(password)
   
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hashed, password)

    def repr(self):
        return f"""User('{self.username}', '{self.email}')"""