#!/usr/bin/python3
"""web views"""

# Import the Flask Blueprint class
from flask import Blueprint, render_template
from models import storage

# Create a blueprint for the web views
web_views = Blueprint('web_views', __name__)

# Define the routes for the web views
@web_views.route('/strains', methods=['GET'], strict_slashes=False)
def strains():
    """Return strains page"""
    all_strains = storage.all('Strain').values()
    # Process the strains data as needed, e.g. sorting or filtering
    return render_template('base.html', strains=all_strains)
