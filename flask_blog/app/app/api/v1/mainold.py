
#import views
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from api.v1.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.v1.views.path import *
app = Flask(__name__)
app.register_blueprint(app_views)
app.config.from_object(Config)
#handles all routes to blog path

db = SQLAlchemy(app)

migrate = Migrate(app, db)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
#from posts.blueprint import posts

#app.register_blueprint(posts, url_prefix='/blog')

@app.teardown_appcontext
def close_db(error):
    """close the session connection when done"""
    db.session.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error handler if the route is wrong"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == '__main__':
    app.run()