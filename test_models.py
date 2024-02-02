# from unittest import TestCase

# from app import app
# from models import db, User


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_ECHO'] = False

# db.drop_all()
# db.create_all()

# class UserModelTestCase(TestCase):
#     """Tests model for users"""

#     def setUp(self):
#         """Clear existing users"""
#         User.query.delete()

#     def tearDown(self):
#         """clean up transations"""
#         db.session.rollback()

#     def test