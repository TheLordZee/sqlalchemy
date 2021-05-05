"""Blogly application."""

from flask import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def reroute():
    return redirect('/users')

@app.route('/users')
def show_list():
    """Shows List of users"""

    users = User.query.all()
    return render_template('home.html', users=users)


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
    return render_template('user.html', user=user)

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

    return redirect('/')