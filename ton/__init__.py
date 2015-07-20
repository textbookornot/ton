from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


app = Flask(__name__, instance_relative_config=True)

# setup configs from default and instance
app.config.from_object('config')
app.config.from_pyfile('config.py')

# psql database
db = SQLAlchemy(app)

# migrations through Flask-Migrate
migrate = Migrate(app, db)

# for hashing user passwords
bcrypt = Bcrypt(app)

# to manage user sessions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

# views and models
from . import views, models
