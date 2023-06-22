#!/usr/bin/env python3
"""Strain Routes for the Flask application"""
# app/routes/strain_routes.py
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Strain
from ..forms import AddStrainForm, UpdateStrainForm, DeleteStrainForm
from .utils import handle_file_upload

strain_routes = Blueprint('strain_routes', __name__, url_prefix='/strains')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'}
MAX_FILE_SIZE = 1.5 * 1024 * 1024  # 1.5 MB
UPLOAD_FOLDER='app/static/images/strain_images/'

@strain_routes.before_request
@login_required
def requires_login():
    pass


@strain_routes.route('/update_strain/<id>', methods=['POST'])
def update_strain(id):
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_PRODUCER')):
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
        if current_user.has_role('CLOUD_CHASER'):
            return redirect(url_for('admin_routes.interface'))
        else:
            return redirect(url_for('main_routes.strains'))


@strain_routes.route('/delete', methods=['POST'])
def delete_strain():
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_PRODUCER')):
        return redirect(url_for('main_routes.index'))
    form = DeleteStrainForm()
    form.strain.choices = [(str(strain.id), strain.name)
                           for strain in Strain.query.all()]
    if form.validate_on_submit():
        strain_to_delete = Strain.query.get(form.strain.data)
        if strain_to_delete:
            db.session.delete(strain_to_delete)
            db.session.commit()
            flash('Strain has been deleted!', 'success')
        else:
            flash('Error: Strain not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))
    return redirect(url_for('admin_routes.interface'))

@strain_routes.route('/add', methods=['POST'])
def add_strain():
    if not (current_user.has_role('CLOUD_CHASER') or current_user.has_role('CLOUD_PRODUCER')):
        return redirect(url_for('main_routes.index'))
    form = AddStrainForm()
    if form.validate_on_submit():
        new_strain = Strain(
            name=form.name.data,
            subtype=form.subtype.data,
            thc_concentration=form.thc_concentration.data,
            cbd_concentration=form.cbd_concentration.data,
        )
        db.session.add(new_strain)
        db.session.commit()
        flash('Your strain has been added!', 'success')
        return redirect(url_for('admin_routes.interface'))
    return redirect(url_for('admin_routes.interface'))
