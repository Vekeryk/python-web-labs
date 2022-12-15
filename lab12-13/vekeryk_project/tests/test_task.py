from flask_login import login_user
from app.todo.models import Category, Task
from test_base import BaseTest
from app.account.models import User

class TaskTest(BaseTest):

    def test_setup(self):
        task = Task.query.filter_by(id=1).first()
        self.assertIsNotNone(task)
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


    def test_task_read(self):
        login_user(User.query.filter_by(id=1).first())
        with self.client:
            response = self.client.get('/tasks/1', follow_redirects=True)
            self.assertIn(b'Test title', response.data)


    def test_task_create(self):
        login_user(User.query.filter_by(id=1).first())
        data = {
            'title': 'Write flask tests',  
            'description': 'New description', 
            'deadline': '2022-12-15',
            'priority': 'low',
            'progress': 'todo',
            'category': 1,
            'owner': 1
        }
        with self.client:
            response = self.client.post('/tasks/create', data=data, 
                        follow_redirects=True)
            self.assertIn(b'New task created', response.data)
            self.assertIn(b'Write flask tests', response.data)


    def test_task_update(self):
        login_user(User.query.filter_by(id=1).first())
        data = {
            'title': 'Updated title',  
            'description': 'Updated description', 
            'deadline': '2022-12-19',
            'priority': 'medium',
            'progress': 'done',
            'category': 1,
            'owner': 1
        }
        with self.client:
            response = self.client.post('/tasks/1/update', data=data, 
                        follow_redirects=True)
            self.assertIn(b'Task has been updated', response.data)
            self.assertIn(b'Updated title', response.data)


    def test_task_delete(self):
        login_user(User.query.filter_by(id=1).first())
        with self.client:
            response = self.client.get('/tasks/1/delete', follow_redirects=True)
            self.assertIn(b'Task has been deleted', response.data)
            task = Task.query.filter_by(id=1).first()
            self.assertIsNone(task)
