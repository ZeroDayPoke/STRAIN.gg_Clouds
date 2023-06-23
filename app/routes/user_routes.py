#!/usr/bin/env python3
"""User Routes for the Flask application"""
# app/routes/user_routes.py
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, User
from ..forms import UpdateUserForm, DeleteUserForm

user_routes = Blueprint('user_routes', __name__, url_prefix='/users')

@user_routes.route('/interface/update_user', methods=['GET', 'POST'])
@login_required
def update_user():
    if not current_user.has_role('ADMIN'):
        return redirect(url_for('main_routes.users'))
    form = UpdateUserForm()
    form.user.choices = [(str(user.id), user.username) for user in User.query.all()]
    if form.validate_on_submit():
        user_to_update = User.query.get(form.user.data)
        if user_to_update:
            user_to_update.username = form.username.data
            user_to_update.email = form.email.data
            db.session.commit()
            flash('User has been updated!', 'success')
        else:
            flash('Error: User not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))

@user_routes.route('/interface/delete_user', methods=['POST'])
@login_required
def delete_user():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.index'))
    form = DeleteUserForm()
    form.user.choices = [(str(user.id), user.username) for user in User.query.all()]
    if form.validate_on_submit():
        user_to_delete = User.query.get(form.user.data)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User has been deleted!', 'success')
        else:
            flash('Error: User not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))
