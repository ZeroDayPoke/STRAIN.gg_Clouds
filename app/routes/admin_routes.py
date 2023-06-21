#!/usr/bin/env python3
"""
admin_routes.py - admin routes for the Flask application
"""
# Path: app/routes/admin_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, User, Role, Store, Strain
from ..forms import AddStoreForm, UpdateStoreForm, DeleteStoreForm, AddStrainForm, DeleteStrainForm
from ..forms import DeleteUserForm, UpdateUserForm, AddUserForm

admin_routes = Blueprint('admin_routes', __name__, url_prefix='')


@admin_routes.route('/presentation', methods=['GET'])
@login_required
def presentation():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.index'))
    return render_template('presentation.html', title='Presentation')

@admin_routes.route('/interface', methods=['GET'])
@login_required
def interface():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.index'))

    users = User.query.all()
    stores = Store.query.all()
    strains = Strain.query.all()

    add_store_form = AddStoreForm()
    update_store_form = UpdateStoreForm()
    delete_store_form = DeleteStoreForm()

    add_strain_form = AddStrainForm()
    delete_strain_form = DeleteStrainForm()

    add_user_form = AddUserForm()
    update_user_form = UpdateUserForm()
    delete_user_form = DeleteUserForm()

    add_store_form.related_strains.choices = [
        (str(strain.id), strain.name) for strain in Strain.query.all()]
    update_store_form.store.choices = [
        (str(store.id), store.name) for store in Store.query.all()]
    update_store_form.related_strains.choices = [
        (str(strain.id), strain.name) for strain in Strain.query.all()]
    delete_store_form.store.choices = [
        (str(store.id), store.name) for store in Store.query.all()]
    delete_strain_form.strain.choices = [
        (str(strain.id), strain.name) for strain in Strain.query.all()]
    delete_user_form.user.choices = [
        (str(user.id), user.username) for user in User.query.all()]
    return render_template('interface.html', title='Interface',
                           add_strain_form=add_strain_form,
                           delete_strain_form=delete_strain_form,
                           add_store_form=add_store_form,
                           update_store_form=update_store_form,
                           delete_store_form=delete_store_form,
                           add_user_form=add_user_form,
                           update_user_form=update_user_form,
                           delete_user_form=delete_user_form, users=users,
                           stores=stores, strains=strains)

@admin_routes.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        role = Role.query.filter_by(name=form.role.data).first()
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully.')
        return redirect(url_for('admin_routes.interface'))
    return render_template('admin_routes.interface', form=form)
