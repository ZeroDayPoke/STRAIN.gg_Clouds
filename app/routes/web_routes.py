#!/usr/bin/python3
"""web views"""

# Import the Flask Blueprint class
from flask import Blueprint, render_template, abort
from models import storage

# Create a blueprint for the web views
web_routes = Blueprint('web_routes', __name__)

# Define the routes for the web views
@web_routes.route('/strains', methods=['GET'], strict_slashes=False)
def strains():
    """Return strains page"""
    all_strains = storage.all('Strain').values()
    # Process the strains data as needed, e.g. sorting or filtering
    return render_template('base.html', strains=all_strains)

@web_routes.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Return index page"""
    return render_template('index.html')

@web_routes.route('/404_test', methods=['GET'], strict_slashes=False)
def not_found_test():
    """Return 404 page test"""
    abort(404)
