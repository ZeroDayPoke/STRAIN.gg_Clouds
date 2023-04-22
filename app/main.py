#!/usr/bin/python3
""" Flask Application """

import sys
import os
from .models import storage
from flask import Flask, render_template
from flask_cors import CORS
from app import app
from app.routes import web_routes, app_routes

# Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Register the routes blueprints with the Flask app
app.register_blueprint(web_routes)
app.register_blueprint(app_routes)

# Apply CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Close storage on app teardown
@app.teardown_appcontext
def close_db(error):
    """Close Storage"""
    storage.close()

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    """ Handle 404 errors """
    return render_template('404.html'), 404

if __name__ == '__main__':
    host = os.environ.get('STRAIN_GG_HOST', '0.0.0.0')
    port = int(os.environ.get('STRAIN_GG_PORT', 5050))
    app.run(host=host, port=port, threaded=True)
