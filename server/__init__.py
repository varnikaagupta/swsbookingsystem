'''
an init file is required for this folder to be considered as a module
'''
from tempfile import template
from flask import Flask
from flask_login import LoginManager
from models.models import Student,db
import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

app = Flask(__name__)
db_string = os.getenv('db_string')

if db_string:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '69cae04b04756f65eabcd2c5a11c8c24'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))