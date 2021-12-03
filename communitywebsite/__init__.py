from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '874efe03260d7d7a4c44d9bc74c14006e8ed9bb9b990c0e75a8e903a66a7dccd30f25e75fae620e6b02d6d1a64a4cf6496ad50a9d3ce8738dbfac9771ce583e5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunity.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from communitywebsite import routes
