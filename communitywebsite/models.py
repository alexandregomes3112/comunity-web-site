from communitywebsite import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id_user):
    return Customer.query.get(int(id_user))


class Customer(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    user_picture = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='author', lazy=True)
    courses = database.Column(database.String, nullable=False, default='Uninformed')

    def posts_counter(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('customer.id'), nullable=False)