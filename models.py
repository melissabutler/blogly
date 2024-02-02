"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    db.create_all()


class User(db.Model):
    """User"""
    __tablename__ = "users"

    def __repr__(self):
        u= self
        return f"<User id={u.id} first_name={u.first_name} last_name{u.last_name}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)
