from app import bcrypt
from . import db

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

        
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(40), unique=False, nullable=False)
   
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password=password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def repr(self):
        return f"""User('{self.username}', '{self.email}')"""