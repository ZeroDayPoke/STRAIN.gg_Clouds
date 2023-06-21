#!/usr/bin/python3
""" Flask Application """
from os import environ
from app import create_app, db
from flask_migrate import Migrate

# Create an instance of the Flask application
app = create_app()

# Create a Migrate instance
migrate = Migrate(app, db)

def run_app():
    """ Main Function """
    host = environ.get('STRAINGG_HOST')
    port = environ.get('STRAINGG_PORT')
    if not host:
        host = '127.0.0.1'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)

if __name__ == "__main__":
    run_app()
