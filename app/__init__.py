#!/usr/bin/env python
"""Initialize Flask app"""

from flask import Flask
from config import config
from flask_login import LoginManager
from app.models import db, User
from .routes import main_routes, store_routes, strain_routes, user_routes, auth_routes, admin_routes

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(main_routes, url_prefix='/clouds/')
    app.register_blueprint(store_routes, url_prefix='/clouds/')
    app.register_blueprint(strain_routes, url_prefix='/clouds/')
    app.register_blueprint(admin_routes, url_prefix='/clouds/')
    app.register_blueprint(auth_routes, url_prefix='/clouds/')
    app.register_blueprint(user_routes, url_prefix='/clouds/')
    app.url_map.strict_slashes = False
    login_manager = LoginManager()
    login_manager.init_app(app)
    db.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Retrieve the user object based on the user_id
        user = User.query.get(user_id)
        return user

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        # Remove the database session after each request
        db.session.remove()

    if app.config.get('OPEN_BROWSER'):
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')

    return app
