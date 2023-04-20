# Description: This file contains the configuration for the app
import os

# Set the base directory for the app
class Config:
    JSONIFY_PRETTYPRINT_REGULAR = True

# Set the development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')

# Set the production configuration
class ProductionConfig(Config):
    DEBUG = False
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')

# Set the configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
