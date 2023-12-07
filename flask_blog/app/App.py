from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timedelta
from flask_security import SQLAlchemyUserDatastore
from flask_babel import Babel
from flask_security import Security
from flask_login import LoginManager
import os



app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
#handles all routes to blog path

db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(minutes=60)
login_manager = LoginManager()
login_manager.login_view = 'posts.login'
login_manager.init_app(app)

from models import *

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

migrate = Migrate(app, db)
babel = Babel(app)
admin = Admin(app)
admin.add_view(ModelView(Tag, db.session))

#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore, login_form=login)
# manager = Manager(app)
# manager.add_commamd('db', MigrateCommand)
# Use the app context to create the database tables
# with app.app_context():
#     if not os.path.exists('Database.db'):
#         db.create_all()
