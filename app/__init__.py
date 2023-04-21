import os
from flask import Flask
from flask_login import LoginManager, current_user
from .models import storage, user
from .config import config

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
