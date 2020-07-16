import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('HELPER_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HELPER_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' # HTML classes to add to login message
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('HELPER_MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('HELPER_MAIL_PASSWORD')
mail = Mail(app)

from helper import routes