#!/usr/bin/python3
"""web views"""

from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session, make_response, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models import user, strain, store
from functools import wraps
from ..models.user import User, UserRole
from sqlalchemy.orm import joinedload

web_routes = Blueprint('web_routes', __name__, url_prefix='/clouds', template_folder='templates', static_folder='static')

login_manager = LoginManager()

def role_helper():
    if current_user.is_authenticated:
        role = current_user.role
    else:
        role = UserRole.CLOUD_GUEST
    return role

def init_app(app):
    """Initialize the login manager with the app"""
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Return the user object for the specified user_id"""
    return current_app.storage.get(user.User, user_id)

@web_routes.route('/strains', methods=['GET'], strict_slashes=False)
def strains():
    """Return strains page"""
    all_strains = current_app.storage.all(strain.Strain)
    role = role_helper()
    return render_template('strains.html', strains=all_strains, user_role=role.value,
                           user_roles={key: value.value for key, value in UserRole.__members__.items()})

@web_routes.route('/stores', methods=['GET'], strict_slashes=False)
def stores():
    """Return stores page"""
    all_dispensaries = current_app.storage.all(store.Store)
    role = role_helper()
    user_id = current_user.id if current_user.is_authenticated else 'NA'
    return render_template('stores.html', stores=all_dispensaries, user_role=role.value,
                           user_roles={key: value.value for key, value in UserRole.__members__.items()},
                           user_id=user_id)

@web_routes.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Return index page"""
    role = role_helper()
    return render_template('index.html', user_role=role.value,
                           user_roles={key: value.value for key, value in UserRole.__members__.items()})

@web_routes.route('/faq', methods=['GET'], strict_slashes=False)
def faq():
    """Return FAQ page"""
    return render_template('faq.html')

@web_routes.route('/about', methods=['GET'], strict_slashes=False)
def about():
    """Return about page"""
    return render_template('about.html')

@web_routes.route('/contact', methods=['GET'], strict_slashes=False)
def contact():
    """Return contact page"""
    return render_template('contact.html')

@web_routes.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """Return the signup page or process the signup form submission"""
    if request.method == 'POST':
        # Get the user information from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role_value = request.form.get('role')

        if role_value == str(UserRole.CLOUD_PRODUCER.value):
            role = UserRole.CLOUD_PRODUCER
        elif role_value == str(UserRole.CLOUD_VENDOR.value):
            role = UserRole.CLOUD_VENDOR
        else:
            role = UserRole.CLOUD_CONSUMER

        # Check if a user with the same username already exists
        all_users = current_app.storage.all(user.User)
        existing_user = next((u for u in all_users if u.username == username), None)
        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('web_routes.signup'))

        # Instantiate a new User object
        new_user = user.User(username=username, email=email, password=password, role=role)

        # Save the new user to the database
        storage.new(new_user)
        storage.save()

        # Redirect to a success page or the home page
        return redirect(url_for('web_routes.index'))

    # Render the signup form template
    return render_template('signup.html', UserRole=UserRole)


@web_routes.route('/signin', methods=['GET', 'POST'], strict_slashes=False)
def signin():
    """Return the signin page or process the signin form submission"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        all_users = storage.all(user.User)
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
    """Sign out the current user and redirect to the home page"""
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('web_routes.index'))

@web_routes.route('/account/<string:user_id>', methods=['GET'], strict_slashes=False)
@login_required
def account(user_id):
    """Return the account page for the specified user"""
    if current_user.id == user_id:
        user_account = current_app.storage.get(User, user_id, relationships=['favorite_strains'])
        favorite_strains = user_account.favorite_strains
        role = user_account.role
        return render_template('account.html',
                               email=user_account.email,
                               favorite_strains=favorite_strains,
                               role=role)
    else:
        flash('You do not have permission to access this page.')
        return redirect(url_for('web_routes.index'))

@web_routes.route('/remove_favorite', methods=['POST'])
@login_required
def remove_favorite():
    """route to remove a favorite strain from the user's favorites"""
    strain_id = request.form.get('strain_id')
    if strain_id:
        favorite_strain = storage.get("Strain", strain_id)
        if favorite_strain:
            current_user.remove_favorite_strain(favorite_strain)
            storage.save()
            flash(f"Removed {favorite_strain.name} from your favorites.", "success")
        else:
            flash("Invalid strain ID.", "error")
    else:
        flash("No strain ID provided.", "error")
    return redirect(url_for('web_routes.account', user_id=current_user.id))
