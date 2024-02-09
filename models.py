"""Models for Blogly."""

import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"


class User(db.Model):
    """User"""
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name{u.last_name}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg")
    # relationship navigation

    # User > posts, casdcade delete
    posts = db.relationship("Post", backref="user", cascade="all, delete", passive_deletes=True)



    @property
    def full_name(self):
        """Return first and last name together"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post. A user can make many posts"""
    __tablename__ = "posts"
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="CASCADE"),
                        nullable=False)
    
    posttags = db.relationship('PostTag', cascade='all, delete', passive_deletes=True)

class PostTag(db.Model):
    """ Mapping a tag to a post"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id", ondelete="CASCADE"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id", ondelete="CASCADE"),
                       primary_key=True)
    
class Tag(db.Model):
    """ Tag groups for posts"""
    __tablename__ = "tags"

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    name= db.Column(db.Text,
                     unique=True)
    
    # relationship navigation
    # Nav Tag > Post > PostTag > Tag
    posts = db.relationship(
        'Post',
          secondary='post_tags',
            cascade="all,delete",
              backref='tags')


   
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    db.create_all()

