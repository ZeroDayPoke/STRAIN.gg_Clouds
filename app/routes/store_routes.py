#!/usr/bin/env python3
"""Store Routes for the Flask application"""
# app/routes/store_routes.py
from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Store
from ..forms import AddStoreForm, UpdateStoreForm, DeleteStoreForm

store_routes = Blueprint('store_routes', __name__, url_prefix='/stores')

@store_routes.before_request
@login_required
def requires_login():
    pass

@store_routes.route('/interface/update_store', methods=['GET', 'POST'])
def update_store():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.stores'))
    form = UpdateStoreForm()
    form.store.choices = [(str(store.id), store.name) for store in Store.query.all()]
    if form.validate_on_submit():
        store_to_update = Store.query.get(form.store.data)
        if store_to_update:
            store_to_update.name = form.name.data
            store_to_update.location = form.location.data
            store_to_update.operating_hours = form.operating_hours.data
            db.session.commit()
            flash('Store has been updated!', 'success')
        else:
            flash('Error: Store not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))

@store_routes.route('/interface/delete_store', methods=['POST'])
def delete_store():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.stores'))
    form = DeleteStoreForm()
    form.store.choices = [(str(store.id), store.name) for store in Store.query.all()]
    if form.validate_on_submit():
        store_to_delete = Store.query.get(form.store.data)
        if store_to_delete:
            db.session.delete(store_to_delete)
            db.session.commit()
            flash('Store has been deleted!', 'success')
        else:
            flash('Error: Store not found.', 'danger')
        return redirect(url_for('admin_routes.interface'))

@store_routes.route('/interface/add_store', methods=['GET', 'POST'])
def add_store():
    if not current_user.has_role('CLOUD_CHASER'):
        return redirect(url_for('main_routes.stores'))
    form = AddStoreForm()
    if form.validate_on_submit():
        new_store = Store(
            name=form.name.data,
            location=form.location.data,
            operating_hours=form.operating_hours.data
        )
        db.session.add(new_store)
        db.session.commit()
        flash('Your store has been added!', 'success')
        return redirect(url_for('admin_routes.interface'))
    return redirect(url_for('admin_routes.interface'))
