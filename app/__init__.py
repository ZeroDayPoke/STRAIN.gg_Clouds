from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from app.web_views.web_routes import web_routes
from app.api.v1.views import api_routes_v1, init_app as init_api_views
from config import config
import uuid

# Create instances of the SQLAlchemy and LoginManager
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_name])
    app.config['SWAGGER'] = {
        'title': 'STRAINGG API',
        'uiversion': 1
    }
    
    # Initialize SQLAlchemy and LoginManager with the Flask application
    db.init_app(app)
    login_manager.init_app(app)

    # Register the blueprints
    init_api_views(app)
    app.register_blueprint(api_routes_v1)
    app.register_blueprint(web_routes)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.before_request
    def before_request():
        if not request.path.startswith('/static/'):
            g.cache_id = str(uuid.uuid4())
            
    if app.config.get('OPEN_BROWSER'):
        import webbrowser
        webbrowser.open('http://127.0.0.1:5000')

    return app

@login_manager.user_loader
def load_user(user_id):
    """Return the user object for the specified user_id"""
    from app.models.user import User  # Avoid circular imports
    return User.query.get(int(user_id))
