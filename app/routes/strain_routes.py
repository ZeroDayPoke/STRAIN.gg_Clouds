#!/usr/bin/env python3
"""Strain Routes for the Flask application"""
# app/routes/strain_routes.py
from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import db, Strain, Store
from ..forms import AddStrainForm, UpdateStrainForm, DeleteStrainForm
from .utils import handle_file_upload

strain_routes = Blueprint('strain_routes', __name__, url_prefix='/strains')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'}
MAX_FILE_SIZE = 1.5 * 1024 * 1024  # 1.5 MB
UPLOAD_FOLDER = 'app/static/images/strain_images/'


@strain_routes.before_request
@login_required
def requires_login():
    pass


@strain_routes.route('/update_strain/<id>', methods=['POST'])
def update_strain(id):
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CULTIVATOR')):
        return redirect(url_for('main_routes.index'))
    form = UpdateStrainForm()
    form.strain.choices = [(str(strain.id), strain.name)
                           for strain in Strain.query.all()]
    if form.validate_on_submit():
        strain_to_update = Strain.query.get(form.strain.data)
        if strain_to_update:
            strain_to_update.name = form.name.data
            strain_to_update.subtype = form.subtype.data
            strain_to_update.thc_concentration = form.thc_concentration.data
            strain_to_update.cbd_concentration = form.cbd_concentration.data
            db.session.commit()
            flash('Strain has been updated!', 'success')
        else:
            flash('Error: Strain not found.', 'danger')
    return redirect(url_for('main_routes.strains'))


@strain_routes.route('/delete_strain/<id>', methods=['POST'])
def delete_strain(id):
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CULTIVATOR')):
        return redirect(url_for('main_routes.index'))
    strain_to_delete = Strain.query.get(id)
    if strain_to_delete:
        db.session.delete(strain_to_delete)
        db.session.commit()
        flash('Strain has been deleted!', 'success')
    else:
        flash('Error: Strain not found.', 'danger')
    return redirect(url_for('main_routes.strains'))


@strain_routes.route('/add_strain', methods=['POST'])
def add_strain():
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_CULTIVATOR')):
        return redirect(url_for('main_routes.index'))

    stores = Store.query.all()
    form = AddStrainForm()
    form.related_stores.choices = [(store.id, store.name) for store in stores]

    if form.validate_on_submit():
        new_strain = Strain()
        image_filename = handle_file_upload(
            request, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE)

        if image_filename is not None:
            new_strain.image_filename = image_filename
        new_strain.name = form.name.data
        new_strain.subtype = form.subtype.data
        new_strain.thc_concentration = form.thc_concentration.data
        new_strain.cbd_concentration = form.cbd_concentration.data
        store_ids = form.related_stores.data
        stores = Store.query.filter(Store.id.in_(store_ids)).all()
        new_strain.related_stores = stores
        db.session.add(new_strain)
        db.session.commit()
        flash('Your strain has been added!', 'success')
    return redirect(url_for('main_routes.strains'))
