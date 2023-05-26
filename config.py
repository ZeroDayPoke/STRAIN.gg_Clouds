# Configuration file for the app

import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Set the base directory for the app
class Config:
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Set the development configuration
class DevelopmentConfig(Config):
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
    OPEN_BROWSER = False
    DB_USER = os.getenv('DB_USER', 'dev_user')
    DB_PASS = os.getenv('DB_PASS', 'dev_pass')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'dev_db')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Set the production configuration
class ProductionConfig(Config):
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
    OPEN_BROWSER = False
    DB_USER = os.getenv('DB_USER', 'prod_user')
    DB_PASS = os.getenv('DB_PASS', 'prod_pass')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'prod_db')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Set the configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
