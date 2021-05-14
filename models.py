from flask_sqlalchemy import *
from datetime import *

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, img_url={u.img_url}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    
    last_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    

    img_url = db.Column(db.String(),
                        default='/static/default.png')

    posts = db.relationship('Post', 
                            passive_deletes=True,
                            backref='user')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post {p.id}, title={p.title}, created_at={p.created_at}, user={p.user.get_full_name()}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text,
                        nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default = datetime.now())

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', 
                                    ondelete="CASCADE"))
    
    tags = db.relationship('Tag',
                            secondary="posts_tags",
                            backref='posts')
    
    post_tags = db.relationship('PostTag',
                                backref='posts',
                                cascade="all, delete",
                                passive_deletes=True) 
    
    
class Tag(db.Model):
    """Tag model"""

    __tablename__="tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.Text,
                    nullable=False,
                    unique=True)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

    tag_posts = db.relationship('PostTag',
                                backref='tags',
                                cascade="all, delete",
                                passive_deletes=True)

class PostTag(db.Model):
    """M2M Relationship model between post and tags"""

    __tablename__="posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id',
                        ondelete="CASCADE"),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id',
                        ondelete="CASCADE"),
                        primary_key=True)