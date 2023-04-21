#!/usr/bin/python3
"""web views"""

# Import the Flask and model modules
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models import storage, user, strain

# Create a blueprint for the web views
web_routes = Blueprint('web_routes', __name__, url_prefix='/clouds')


# Create a login manager instance
login_manager = LoginManager()


# Initialize the login manager with the app
def init_app(app):
    login_manager.init_app(app)


# Load the user from the user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return storage.get(user.User, user_id)


# Define the routes for the web views
@web_routes.route('/strains', methods=['GET'], strict_slashes=False)
def strains():
    """Return strains page"""
    all_strains = storage.all('Strain').values()
    # Process the strains data as needed, e.g. sorting or filtering
    return render_template('strains.html', strains=all_strains)


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
        existing_user = next((u for u in all_users if u.username == username), None)
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


@web_routes.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        all_users = storage.all(user.User).values()
        existing_user = next((u for u in all_users if u.username == username), None)

        if existing_user and check_password_hash(existing_user.password, password):
            login_user(existing_user)
            flash('Successfully logged in.')
            return redirect(url_for('web_routes.index'))
        else:
            flash('Invalid username or password.')

    return render_template('signin.html')


@web_routes.route('/signout', methods=['GET'], strict_slashes=False)
@login_required
def signout():
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('web_routes.index'))
