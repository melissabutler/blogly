"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
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
    if first_name == "":
        flash("Please enter a first name.", "ERROR")

    last_name = request.form["last_name"]
    if last_name == "":
        flash("Please enter a last name.", "ERROR") 

    else:
        image_url = request.form["image_url"]
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        flash("New user added.", "SUCCESS")
        return redirect(f'/users/{new_user.id}')
    return redirect('/users/new')
    

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
        flash('Please enter a first name', 'ERROR')
    user.last_name = request.form["last_name"]
    if user.last_name == "":
        flash("Please enter a last name", "ERROR")
    user.image_url = request.form["image_url"]
    if user.image_url == "":
        flash("Please update image url", "ERROR")
    
    else:
        db.session.add(user)
        db.session.commit()
        flash("User successfully edited", "SUCCESS")
        return redirect(f'/users/{user_id}')
    return redirect(f'/users/{user_id}/edit')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted", "SUCCESS")
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
    if title == "":
        flash("Please enter a title", "ERROR")
    content= request.form["content"]
    if content =="":
        flash("Please enter some content", "ERROR")
    else:
        user=user
        new_post = Post(title = request.form["title"],
                    content= request.form["content"],
                    user=user)
        db.session.add(new_post)
        db.session.commit()
        flash("Post successfully created", "SUCCESS")
        return redirect(f"/users/{user_id}")
    return redirect(f"/users/{user_id}/posts/new")

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
    if post.title == "":
        flash("Please submit new title", "ERROR")
    post.content = request.form["content"]
    if post.content == "":
        flash("Please enter new post content", "ERROR")
    else:
        db.session.add(post)
        db.session.commit()
        flash("Post successfully edited", "SUCCESS")
        return redirect(f'/posts/{post_id}')
    return redirect(f'/posts/{post_id}/edit')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post= Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted", "SUCCESS")
    
    return redirect('/users')