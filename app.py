"""Blogly application."""

from flask import *
from models import *
from datetime import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'h7f4oubh487fbybqp8YE9P'

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('home.html', posts=posts)

@app.route('/users')
def show_list():
    """Shows List of users"""

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new-user')
def new_user():
    """Allows for the creation of new users"""

    return render_template('user-form.html')

@app.route('/users/new-user', methods=["POST"])
def make_user():
    """Makes new user and adds it to database"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    url = request.form['img-url']
    if url == '':
        url = "/static/default.png"
        if first_name == '':
            flash('First Name Required')
    
    if last_name == '':
        flash('Last Name required')

    if (first_name == "") or (last_name == ""):
        return redirect(f'/users/new-user')

    new_user = User(first_name=first_name, 
                    last_name=last_name, 
                    img_url=url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Shows detail about a user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user_id).all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """Shows form to allow user to edit user"""

    user = User.query.get(user_id)
    return render_template('edit-form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edits user"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    url = request.form['img-url']
    if url == '':
        url = "/static/default.png"

    if first_name == '':
        flash('First Name Required')
    
    if last_name == '':
        flash('Last Name required')

    if (first_name == "") or (last_name == ""):
        return redirect(f'/users/{user_id}/edit')
    
    user_edit = User.query.get(user_id)
    user_edit.first_name = first_name
    user_edit.last_name = last_name
    user_edit.img_url = url

    db.session.add(user_edit)
    db.session.commit()

    return redirect(f'/users/{user_edit.id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Removes User from database"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Displays Post """

    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows form to make new post"""

    user = User.query.get_or_404(user_id)
    return render_template('post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Saves the new post"""

    title = request.form['title-form']
    content = request.form['content-form']
    if title == '':
        flash('Title Required')
    
    if content == '':
        flash('Content required')

    if (content == "") or (title == ""):
        return redirect(f'/users/{user_id}/posts/new') 

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Displays form to edit post"""

    post = Post.query.get(post_id)
    return render_template('post-edit-form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Saves the edit"""

    title = request.form['title-form']
    content = request.form['content-form']
    if title == '':
        flash('Title Required')
    
    if content == '':
        flash('Content required')

    if (content == "") or (title == ""):
        return redirect(f'/posts/{{post_id}}/edit') 

    edit_post = Post.query.get(post_id)
    edit_post.title = title
    edit_post.content = content

    db.session.add(edit_post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes post"""

    post = Post.query.get(post_id)
    user_id = post.user_id

    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')
