from unittest import TestCase

from app import app
from models import db, User



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO']= False


app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests users views"""

    def setUp(self):
        """Sets up a sample user"""
        User.query.delete()

        user = User(first_name='Test', last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up after run"""
        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            response = client.get('/users/1')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Test User's Details</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "Test", "last_name": "User"}
            response = client.post('/users/new', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>Test User's Details</h1>", html)