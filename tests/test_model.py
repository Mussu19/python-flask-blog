import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = app  # Use the app instance directly
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()  # Clean up session
            db.drop_all()
            
    def test_user_creation(self):
        with self.app.app_context():
            new_user = User(username='user', password='admin@12')
            db.session.add(new_user)
            db.session.commit()

            queried_user = User.query.filter_by(username='user').first()
            self.assertIsNotNone(queried_user)
            self.assertEqual(queried_user.password, 'admin@12')

if __name__ == '__main__':
    unittest.main()