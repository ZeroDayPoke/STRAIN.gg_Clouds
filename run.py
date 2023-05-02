#!/usr/bin/python3
""" Flask Application """

from os import environ
from flask import make_response, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
from sqlalchemy.orm.session import SessionTransactionState
from config import config
from app import create_app

# Set the environment
env = environ.get('FLASK_MODE', 'default')
app = create_app(config[env])

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

def run_app():
    """ Main Function """
    host = environ.get('STRAINGG_HOST')
    port = environ.get('STRAINGG_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)

if __name__ == "__main__":
    run_app()
