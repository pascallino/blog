from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os




app = Flask(__name__)
app.config.from_object(Config)

#handles all routes to blog path

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_commamd('db', MigrateCommand)
# Use the app context to create the database tables
# with app.app_context():
#     if not os.path.exists('Database.db'):
#         db.create_all()
