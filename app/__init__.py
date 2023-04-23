import os
from flask import Flask
from flask_login import LoginManager, current_user
from .models import storage, user
from .config import config
from app.routes import web_routes, app_routes

app = Flask(__name__, static_folder="static")
app.secret_key = 'supersecretkey'
app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])

# Configure Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return storage.get(user.User, user_id)

@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__, static_folder="static")
    app.secret_key = 'supersecretkey'
    app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])
    # Register the routes blueprints with the Flask app
    app.register_blueprint(web_routes)
    app.register_blueprint(app_routes)

    # Configure Login Manager
    login_manager.init_app(app)

    @app.context_processor
    def inject_current_user():
        return dict(current_user=current_user)

    return app
