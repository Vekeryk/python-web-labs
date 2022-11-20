from flask_login import UserMixin
from .. import db, bcrypt, login_manager

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
        self.password_hashed = bcrypt.generate_password_hash(password)
   
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hashed, password)

    def repr(self):
        return f"""User('{self.username}', '{self.email}')"""


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))