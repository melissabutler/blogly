from unittest import TestCase

from app import app
from models import db, User, Post



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

        user = User(id=1, first_name='Test', last_name="User")
        
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        Post.query.delete()

        test_post = Post(title="Hi", content="This is a test", user_id=1)
        db.session.add(test_post)
        db.session.commit()

    def tearDown(self):
        """Delete test users and posts from database after run"""
        User.query.delete()
        Post.query.delete()
        db.session.commit()

    def test_show_user_list(self):
        """Test render of user list"""
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        """ Test user detail page"""
        with app.test_client() as client:
            response = client.get('/users/1')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="h1">Test User</h1>', html)

    def test_home(self):
        """Test render of home page"""
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Home', html)

    def test_add_user(self):
        """Test successful addition of new user"""
        User.query.delete()
        db.session.commit()

        with app.test_client() as client:
            data = {
                "first_name": "Add Test",
                "last_name": "User",
                "image_url": "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"
            }

            response = client.post("/users/new", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)


    def test_show_post_form(self):
        """Test render of post form"""
        with app.test_client() as client:
            response = client.get('/users/1/posts/new')
            html = response.get_data(as_text=True)

            self.assertIn('<h2>Add Post for Test User</h2>', html)
            self.assertEqual(response.status_code, 200)

    def test_add_post(self):
            """Test successful addition of new post"""
            Post.query.delete()
            db.session.commit()

            with app.test_client() as client:
                data = {
                    "title": "Test Post",
                    "content": "This is a test post",
                    "user_id": 1           
                    }

                response = client.post("/users/1/posts/new", data=data, follow_redirects=True)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
