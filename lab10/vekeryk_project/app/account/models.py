from flask_login import UserMixin
from sqlalchemy import case
from ..todo.models import Task
from .. import db, bcrypt, login_manager

assosiation_table = db.Table(
    'task_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
)
task_order = "case(value=Task.priority, whens={'low': 2, 'medium':1, 'high':0}), Task.created"

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password_hashed = db.Column(db.String(40), unique=False, nullable=False)
    
    own_tasks = db.relationship("Task", backref="owner", order_by=task_order)
    collaborate_tasks = db.relationship('Task', secondary=assosiation_table, backref=db.backref('collaborators'), order_by=task_order)

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
