from .. import db
from sqlalchemy.sql.functions import now
import enum


class Priority(enum.Enum):
    low = 1
    medium = 2
    high = 3


class Progress(enum.Enum):
    todo = 1
    doing = 2
    done = 3


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=now())
    modified = db.Column(db.DateTime, default=now(), onupdate=now())
    deadline = db.Column(db.Date, default=now())

    priority = db.Column(db.Enum(Priority), default='low')
    progress = db.Column(db.Enum(Progress), default='todo')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    category = db.relationship("Category", backref="tasks")
    comments = db.relationship('Comment', backref="task")

    def repr(self):
        return f"<Task {self.id} {self.title} {self.description} {self.created}" \
            + f"{self.modified} {self.deadline} {self.priority} {self.progress}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def repr(self):
        return f"<Category {self.id} {self.name}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))    

    user = db.relationship('User', backref=db.backref('comments'))
