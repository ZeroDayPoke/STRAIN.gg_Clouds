#!/usr/bin/env python3
"""Auth Routes for the app"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from ..models import db, User, Role
from ..forms import SignupForm, SigninForm

auth_routes = Blueprint('auth_routes', __name__, url_prefix='/auth')

@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        role_name = form.role.data
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)
        else:
            flash('Invalid role selected. Please try again.')
            return render_template('signup.html', form=form)

        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main_routes.index'))
    return render_template('signup.html', form=form)



@auth_routes.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Successfully signed in.')
        return redirect(url_for('main_routes.index'))
    return render_template('signin.html', form=form)

@auth_routes.route('/signout', methods=['GET'])
@login_required
def signout():
    """Sign out the current user and redirect to the home page"""
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('main_routes.index'))


@auth_routes.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html', current_user=current_user)


@auth_routes.route('/send_verification_email', methods=['GET'])
@login_required
def send_verification_email():
    user_email = current_user.email

    response = request.post('http://localhost:3000/send-email', json={'to': user_email})

    if response.status_code == 200:
        token = response.json()['token']
        current_user.verification_token = token
        db.session.commit()

        return 'Verification email sent! Check your inbox for the verification link.'
    else:
        return 'There was an error sending the verification email. Please try again later.', 500
