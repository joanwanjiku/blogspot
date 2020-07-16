from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    hash_password = db.Column(db.String(255))

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

