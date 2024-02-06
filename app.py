"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)


@app.route('/')
def home_page():
    """Shows home page"""
    users = User.query.all()
    posts = Post.query.all()
    return render_template('home.html', users=users, posts=posts)

@app.route('/users')
def show_user_list():
    """ Shows list of users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def user_form():
    """Shows new user form"""
    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """ Redirects to user details after form submisson"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ Show details about user """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template('user_details.html', user=user,posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edits user details"""
    user= User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    if user.first_name == "":
        print('First name error')
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

# POST ROUTES#######################################

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows new post form from user page"""
    user= User.query.get_or_404(user_id)
    return render_template("post_form.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Handles new post form submission"""
    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content= request.form["content"]
    

    new_post = Post(title = request.form["title"],
                    content= request.form["content"],
                    user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows post """
    
    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Shows form for editing post details"""
    post= Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edits post details"""
    post= Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post= Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    
    return redirect('/users')