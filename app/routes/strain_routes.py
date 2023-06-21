#!/usr/bin/env python3
"""Strain Routes for the Flask application"""
# app/routes/strain_routes.py
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Strain
from ..forms import AddStrainForm, UpdateStrainForm, DeleteStrainForm

strain_routes = Blueprint('strain_routes', __name__, url_prefix='')

@strain_routes.route('/interface/update_strain', methods=['GET', 'POST'])
@login_required
def update_strain():
    if not current_user.has_role('ADMIN'):
        return redirect(url_for('main_routes.strains'))
    form = UpdateStrainForm()
    form.strain.choices = [(str(strain.id), strain.name) for strain in Strain.query.all()]
    if form.validate_on_submit():
        strain_to_update = Strain.query.get(form.strain.data)
        if strain_to_update:
            strain_to_update.name = form.name.data
            strain_to_update.type = form.type.data
            strain_to_update.delta_nine_concentration = form.delta_nine_concentration.data
            strain_to_update.cbd_concentration = form.cbd_concentration.data
            strain_to_update.terpene_profile = form.terpene_profile.data
            strain_to_update.effects = form.effects.data
            strain_to_update.uses = form.uses.data
            strain_to_update.flavor = form.flavor.data
            db.session.commit()
            flash('Strain has been updated!', 'success')
        else:
            flash('Error: Strain not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))

@strain_routes.route('/interface/delete_strain', methods=['POST'])
@login_required
def delete_strain():
    if not current_user.has_role('ADMIN'):
        return redirect(url_for('main_routes.strains'))
    form = DeleteStrainForm()
    form.strain.choices = [(str(strain.id), strain.name) for strain in Strain.query.all()]
    if form.validate_on_submit():
        strain_to_delete = Strain.query.get(form.strain.data)
        if strain_to_delete:
            db.session.delete(strain_to_delete)
            db.session.commit()
            flash('Strain has been deleted!', 'success')
        else:
            flash('Error: Strain not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))

@strain_routes.route('/interface/add_strain', methods=['GET', 'POST'])
@login_required
def add_strain():
    if not current_user.has_role('ADMIN'):
        return redirect(url_for('main_routes.strains'))
    form = AddStrainForm()
    if form.validate_on_submit():
        new_strain = Strain(
            name=form.name.data,
            type=form.type.data,
            delta_nine_concentration=form.delta_nine_concentration.data,
            cbd_concentration=form.cbd_concentration.data,
            terpene_profile=form.terpene_profile.data,
            effects=form.effects.data,
            uses=form.uses.data,
            flavor=form.flavor.data
        )
        db.session.add(new_strain)
        db.session.commit()
        flash('Your strain has been added!', 'success')
        return redirect(url_for('admin_routes.interface'))
    return redirect(url_for('admin_routes.interface'))
