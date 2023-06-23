#!/usr/bin/env python3
"""
config.py - Configuration file for the app
"""
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPEN_BROWSER = False
    DB_USER = os.getenv('DB_USER', 'dev_user')
    DB_PASS = os.getenv('DB_PASS', 'dev_pass')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'dev_db')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Set the development configuration
class DevelopmentConfig(Config):
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)

# Set the production configuration
class ProductionConfig(Config):
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)

# Set the configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
