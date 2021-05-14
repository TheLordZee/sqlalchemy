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
def show_users():
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
    
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template('post-form.html',
                            user=user, 
                            tags=tags)

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

    new_post = Post(title=title, 
                    content=content, 
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    all_tags = Tag.query.all()
    post_tags = []
    for tag in all_tags:
        if request.form.get(f"{tag.name}"):
            post_tags.append(tag)

    for tags in post_tags:
        db.session.add(PostTag(post_id=new_post.id, tag_id=tags.id))
    
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    """Displays form to edit post"""

    tags = Tag.query.all()
    post = Post.query.get(post_id)
    return render_template('post-edit-form.html',   
                            post=post,
                            tags=tags)

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

    all_tags = Tag.query.all()
    post_tags = []
    for tag in all_tags:
        if request.form.get(f"{tag.name}"):
            post_tags.append(tag)

    for tags in post_tags:
        if PostTag.query.get((post_id, tags.id)) == None:
            db.session.add(PostTag(post_id=post_id, tag_id=tags.id))
    
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

@app.route('/tags')
def show_tags():
    """Shows list of tags"""

    tags = Tag.query.all()
    return render_template("tags-list.html", tags=tags)

@app.route('/tags/new-tag')
def new_tag():
    """Allows users to make tags"""

    return render_template('new-tag.html')

@app.route('/tags/new-tag', methods=['POST'])
def submit_tag():
    """Submits and saves new tags"""

    name = request.form['name']
    if name == '':
        flash('Name required!')
        return redirect('/tags/new-tag')
    
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows tag info"""

    tag = Tag.query.get(tag_id)
    num_posts = len(tag.posts)
    return render_template('tag.html', tag=tag, num_posts=num_posts)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Shows form to edit a tag"""

    tag = Tag.query.get(tag_id)
    return render_template('edit-tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    """Checks and submits edit to database"""
    
    tag = Tag.query.get(tag_id)
    name = request.form['name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Deletes tag and removes it from the database"""

    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()

    return redirect('/tags')
