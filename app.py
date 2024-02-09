"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    """Shows home page"""
    users = User.query.all()
    posts = Post.query.limit(5).all()
    return render_template('home.html', users=users, posts=posts)

###################### USER ROUTES ###############################

@app.route('/users')
def show_user_list():
    """ Shows list of users"""
    users = User.query.all()
    return render_template('/user/users.html', users=users)

@app.route('/users/new')
def user_form():
    """Shows new user form"""
    return render_template('/user/form.html')

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
    return render_template('/user/details.html', user=user,posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template('/user/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edits user details"""
    user= User.query.get_or_404(user_id)

    new_first_name = request.form["first_name"]
    if new_first_name != "":
        user.first_name = new_first_name
        flash("User first name edited", "SUCCESS")
    new_last_name = request.form["last_name"]
    if new_last_name != "":
        user.last_name = new_last_name
        flash("User last name updated", "SUCCESS")
    new_image_url = request.form["image_url"]
    if new_image_url != "":
        user.image_url = new_image_url
        flash("User image updated", "SUCCESS")
    
  
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash("User deleted", "SUCCESS")
    return redirect('/users')

########################################POST ROUTES#######################################

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows new post form from user page"""
    user= User.query.get_or_404(user_id)
    tags= Tag.query.all()
    return render_template("/post/form.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Handles new post form submission"""


    user = User.query.get_or_404(user_id)
    taglist = request.form.getlist("tags")
    tag_ids = [int(num) for num in taglist]
    tags= Tag.query.filter(Tag.id.in_(tag_ids)).all()
    

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
                    user=user,
                    tags=tags)
        db.session.add(new_post)
        db.session.commit()
        flash("Post successfully created", "SUCCESS")
        return redirect(f"/users/{user_id}")
    return redirect(f"/users/{user_id}/posts/new")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows post """
    
    post = Post.query.get_or_404(post_id)

    return render_template('/post/details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Shows form for editing post details"""
    post= Post.query.get_or_404(post_id)
    tags= Tag.query.all()
    return render_template('/post/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edits post details"""
    post= Post.query.get_or_404(post_id)

    taglist = request.form.getlist("tags")
    tag_ids = [int(num) for num in taglist]
    tags= Tag.query.filter(Tag.id.in_(tag_ids)).all()

# If no new content is added, keep old content
    new_title = request.form["title"]
    if new_title != "":
        post.title = new_title
        flash("Post title edited", "SUCCESS")
    new_content = request.form["content"]
    if new_content != "":
        post.content = new_content
        flash("Post content edited", "SUCCESS")

    post.tags = tags
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post= Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted", "SUCCESS")
    
    return redirect('/users')

############################## TAG ROUTES ############################

@app.route('/tags')
def show_tags():
    """ Shows list of all tags"""
    tags = Tag.query.all()
    return render_template('/tag/tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """ Shows detail of a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tag/details.html', tag=tag)

@app.route('/tags/new')
def show__tag_form():
    """Shows form for new tag"""
    return render_template('/tag/form.html')

@app.route('/tags/new', methods=['POST'])
def make_new_tag():
    """Handles submission of new tag form"""
    name = request.form["name"]
    if name == "":
        flash("Please enter a valid tag name.", "ERROR")
    else:
        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash("Tag successfully added", "SUCCESS")
        return redirect('/tags')
    return redirect('/tags/new')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """Shows tag edit form"""
    tag= Tag.query.get_or_404(tag_id)
    return render_template('/tag/edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Handles submission of tag-edit form"""
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["name"]

    if tag.name == "":
        flash("Please submit a new tag name", "ERROR")
    else:
        db.session.add(tag)
        db.session.commit()
        flash("Tag successfully updated", "SUCCESS")
        return redirect(f'/tags/{tag_id}')
    return redirect(f'/tags/{tag_id}/edit')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Handles deletion of a tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f'Tag "{tag.name}" deleted', "SUCCESS")

    return redirect('/tags')