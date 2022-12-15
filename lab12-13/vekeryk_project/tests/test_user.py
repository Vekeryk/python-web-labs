from flask import url_for
from flask_login import login_user, current_user
from app import db

from app.account.models import User
from test_base import BaseTest

class UserTest(BaseTest):

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portfolio', response.data)


    def test_save_user(self):
        user = User(username='test', email='test@test.com', password='password')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(user)


    def test_register(self):
        with self.client:
            self.client.post(
                '/register',
                data=dict(username='test', email='test@test.com', password='password', confirm_password='password'),
                follow_redirects=True
            )
        user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(user)

    def test_login_redirect(self):
        response = self.client.get('/account', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location.split('?')[0], url_for('account.login', _external=False))


    def test_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects=True
            )
        self.assertIsNotNone(current_user)
        self.assertEqual(current_user.username, 'user')
        self.assertIn(b'Your account', response.data)


    def test_logout(self):
        user = User.query.filter_by(email='user@gmail.com').first()
        login_user(user)
        self.assertIsNotNone(current_user)
        with self.client:
            response = self.client.get(
                '/logout',
                follow_redirects=True
            )
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b'You have been logged out', response.data)
