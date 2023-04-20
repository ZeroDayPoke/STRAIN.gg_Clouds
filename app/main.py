#!/usr/bin/python3
""" Flask Application """

import sys
import os
# Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Import modules
from models import storage
from routes import web_routes, app_routes
from flask import Flask, render_template
from flask_cors import CORS
from config import config

# Set up template and static folders
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

# Initialize Flask app
app = Flask(__name__, template_folder=template_dir)
app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])

# Register blueprints and apply CORS
app.register_blueprint(web_routes)
app.register_blueprint(app_routes)
CORS(app, resources={r"/*": {"origins": "*"}})

# Close storage on app teardown
@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Run the Flask app
if __name__ == "__main__":
    """ Main Function """
    host = os.environ.get('STRAIN_GG_HOST', '0.0.0.0')
    port = int(os.environ.get('STRAIN_GG_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
