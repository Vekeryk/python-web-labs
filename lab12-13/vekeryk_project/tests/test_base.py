from datetime import datetime
from flask_testing import TestCase
from app.account.models import User
from app.todo.models import Category, Task
from app import create_app, db

class BaseTest(TestCase):
    def create_app(self):
        return create_app(config_name='test')

    def setUp(self):
        db.create_all()
        user = User(username='user', email='user@gmail.com', password='password')
        task = Task(title='Test title', description='Test description', \
                    deadline=datetime.now(), priority='low', progress='todo',
                    category_id=1, owner_id=1)
        category = Category(name='Flask homework')
        db.session.add_all([user, category, task])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()