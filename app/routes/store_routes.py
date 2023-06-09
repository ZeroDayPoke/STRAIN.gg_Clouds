#!/usr/bin/env python3
"""Store Routes for the Flask application"""
# app/routes/store_routes.py
from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import db, Store, Strain
from ..forms import AddStoreForm, UpdateStoreForm, DeleteStoreForm
from .utils import handle_file_upload

store_routes = Blueprint('store_routes', __name__, url_prefix='/stores')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'}
MAX_FILE_SIZE = 1.5 * 1024 * 1024  # 1.5 MB
UPLOAD_FOLDER = 'app/static/images/store_images/'


@store_routes.before_request
@login_required
def requires_login():
    pass


@store_routes.route('/update_store/<id>', methods=['POST'])
def update_store(id):
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CARRIER')):
        return redirect(url_for('main_routes.index'))

    strains = Strain.query.all()
    form = UpdateStoreForm()
    form.related_strains.choices = [
        (strain.id, strain.name) for strain in strains]
    if form.validate_on_submit():
        store = Store.query.get(id)
        image_filename = handle_file_upload(
            request, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE)
        if image_filename is not None:
            store.image_filename = image_filename
        store.name = form.name.data
        store.location = form.location.data
        store.operating_hours = form.operating_hours.data
        store.owner_id = current_user.id
        store.related_strains = Strain.query.filter(
            Strain.id.in_(form.related_strains.data)).all()
        db.session.commit()
        flash('Store updated successfully!', 'success')
    return redirect(url_for('main_routes.stores'))


@store_routes.route('/delete_store/<store_id>', methods=['POST'])
def delete_store(store_id):
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CARRIER')):
        return redirect(url_for('main_routes.index'))
    store_to_delete = Store.query.get(store_id)
    if store_to_delete:
        db.session.delete(store_to_delete)
        db.session.commit()
        flash('Store has been deleted!', 'success')
    else:
        flash('Error: Store not found.', 'danger')
    return redirect(url_for('main_routes.stores'))


@store_routes.route('/add_store', methods=['POST'])
def add_store():
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CARRIER')):
        return redirect(url_for('main_routes.index'))

    strains = Strain.query.all()
    form = AddStoreForm()
    form.related_strains.choices = [
        (strain.id, strain.name) for strain in strains]

    if form.validate_on_submit():
        new_store = Store()
        image_filename = handle_file_upload(
            request, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE)

        if image_filename is not None:
            new_store.image_filename = image_filename
        new_store.name = form.name.data
        new_store.location = form.location.data
        new_store.operating_hours = form.operating_hours.data
        new_store.owner_id = current_user.id

        strain_ids = form.related_strains.data
        strains = Strain.query.filter(Strain.id.in_(strain_ids)).all()
        new_store.related_strains = strains

        db.session.add(new_store)
        db.session.commit()
        flash('Your store has been added!', 'success')
    else:
        flash('Error: Store not added.', 'danger')

    return redirect(url_for('main_routes.stores'))
