#!/usr/bin/env python3
"""Store Routes for the Flask application"""
# app/routes/store_routes.py
from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import db, Store, Strain
from ..forms import AddStoreForm, UpdateStoreForm, DeleteStoreForm

store_routes = Blueprint('store_routes', __name__, url_prefix='/stores')


@store_routes.before_request
@login_required
def requires_login():
    pass


@store_routes.route('/update_store', methods=['POST'])
def update_store():
    form = UpdateStoreForm()
    form.related_strains.choices = [(s.id, s.name) for s in Strain.query.all()]
    if form.validate_on_submit():
        id = form.id.data
        store = Store.query.get(id)
        if store:
            store.name = form.name.data
            store.location = form.location.data
            store.operating_hours = form.operating_hours.data
            store.related_strains = form.related_strains.data
            db.session.commit()
            flash('Store updated successfully', 'success')
            return redirect(url_for('main.stores'))
        else:
            flash('Store not found', 'danger')
            return redirect(url_for('main.stores'))
    else:
        print('Error: {}'.format(form.errors))
        flash('Form validation error', 'error')
        return redirect(url_for('main.stores'))


@store_routes.route('/delete_store', methods=['POST'])
def delete_store():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.index'))
    form = DeleteStoreForm()
    form.store.choices = [(str(store.id), store.name)
                          for store in Store.query.all()]
    if form.validate_on_submit():
        store_to_delete = Store.query.get(form.store.data)
        if store_to_delete:
            db.session.delete(store_to_delete)
            db.session.commit()
            flash('Store has been deleted!', 'success')
        else:
            flash('Error: Store not found.', 'danger')
    if current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('admin_routes.interface'))
    else:
        return redirect(url_for('main_routes.stores'))


@store_routes.route('/add_store', methods=['POST'])
def add_store():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.index'))

    strains = Strain.query.all()
    form = AddStoreForm()
    form.related_strains.choices = [
        (strain.id, strain.name) for strain in strains]

    if form.validate_on_submit():
        new_store = Store()
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
        print(form.errors)
        flash('Error: Store not added.', 'danger')
    if current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('admin_routes.interface'))
    else:
        return redirect(url_for('main_routes.stores'))
