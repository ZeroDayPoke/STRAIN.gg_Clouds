#!/usr/bin/python3
"""web views"""

# Import the Flask and model modules
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from models import storage, user, strain

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

@web_routes.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    if request.method == 'POST':
        # Get the user information from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if a user with the same username already exists
        all_users = storage.all(user.User).values()
        existing_user = sorted(all_users, key=lambda u: u.username)
        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('web_routes.signup'))

        # Instantiate a new User object
        new_user = user.User(username=username, email=email, password=password)
        
        # Save the new user to the database
        storage.new(new_user)
        storage.save()

        # Redirect to a success page or the home page
        return redirect(url_for('web_routes.index'))

    # Render the signup form template
    return render_template('signup.html')
