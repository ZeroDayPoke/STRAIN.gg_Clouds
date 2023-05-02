#!/usr/bin/python3
"""Initialize the Flask app"""

from flask import Flask, g, request, current_app
from flask_login import LoginManager, current_user
from app.models.engine.dbstorage import DBStorage
from app.models.user import UserRole, User
from app.web_views.web_routes import web_views
from app.api.v1.views import api_routes_v1, init_app as init_api_views
import uuid

# Create a login manager instance
login_manager = LoginManager()

# Add a function to return the class_dictionary instance
def get_class_dictionary():
    global class_dictionary
    return class_dictionary

# Add a function to return the storage instance
def get_storage():
    global storage
    return storage

def create_app(config_class=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.secret_key = 'supersecretkey'

    # Set the storage attribute of the app object
    app.storage = DBStorage()
    app.class_dictionary = app.storage.class_dictionary

    if config_class is not None:
        app.config.from_object(config_class)

    init_api_views(app)
    app.register_blueprint(api_routes_v1)

    login_manager.init_app(app)
    app.register_blueprint(web_views)

    @app.teardown_appcontext
    def close_db(error):
        """Close Storage"""
        app.storage.Session.remove()

    @app.before_request
    def before_request():
        if not request.path.startswith('/static/'):
            g.cache_id = str(uuid.uuid4())
            g.user_role = role_helper()

    app.config['SWAGGER'] = {
        'title': 'STRAINGG API',
        'uiversion': 1
    }

    if app.config.get('OPEN_BROWSER'):
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')

    app.storage.reload()

    return app

# Helper function to get or assign a user role
def role_helper():
    if current_user.is_authenticated:
        role = current_user.role
    else:
        role = UserRole.CLOUD_GUEST
    return role

@login_manager.user_loader
def load_user(user_id):
    """Return the user object for the specified user_id"""
    return current_app.storage.get('User', user_id)
