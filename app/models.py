from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    hash_password = db.Column(db.String(255)) 
    bio = db.Column(db.String)
    photo_url = db.Column(db.String)   
    posts = db.relationship('Post', backref= 'users', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('this property cannot be accessed')

    @password.setter
    def password(self, password):
        self.hash_password= generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def add_user(self):        
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_user_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        return user


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted = db.Column(db.DateTime, default=datetime.date.today())
    image_url = db.Column(db.String)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='posts', lazy= 'dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all_posts(cls):
        posts = cls.query.order_by(cls.posted.desc()).all()
        return posts
    
    @classmethod
    def get_post_by_id(cls, id):
        post = cls.query.filter_by(id=id).first()
        return post

    @classmethod
    def get_post_by_userid(cls, user_id):
        posts = cls.query.filter_by(user_id = user_id).all()
        return posts

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_comments(cls, id):
        comments = cls.query.filter_by(post_id = id).all()
        return comments


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)

