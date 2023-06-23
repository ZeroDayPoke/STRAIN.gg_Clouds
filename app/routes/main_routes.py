#!/usr/bin/env python3
"""Main Routes for the Flask application"""
# app/routes/main_routes.py
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from ..models import User, Store, Strain
from ..forms import StrainFilterForm, AddStoreForm, AddStrainForm, UpdateStoreForm, UpdateStrainForm, DeleteStoreForm, DeleteStrainForm

main_routes = Blueprint('main_routes', __name__, url_prefix='')


@main_routes.route('/')
def index():
    return render_template('index.html', include_header=True, current_user=current_user)


@main_routes.route('/about')
def about():
    return render_template('about.html', include_header=True, current_user=current_user)


@main_routes.route('/contact')
def contact():
    return render_template('contact.html', include_header=True, current_user=current_user)


@main_routes.route('/faq')
def faq():
    return render_template('faq.html', include_header=True, current_user=current_user)


@main_routes.route('/users', methods=['GET', 'POST'])
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@main_routes.route('/stores', methods=['GET'])
def stores():
    strains = Strain.query.all()
    stores = Store.query.all()
    add_store_form = AddStoreForm()
    update_store_form = UpdateStoreForm()
    delete_store_form = DeleteStoreForm()
    add_store_form.related_strains.choices = [(strain.id, strain.name) for strain in strains]
    update_store_form.related_strains.choices = [(strain.id, strain.name) for strain in strains]

    return render_template('stores.html', stores=stores,
                           add_store_form=add_store_form,
                           update_store_form=update_store_form,
                           delete_store_form=delete_store_form,
                           current_user=current_user, strains=strains)


@main_routes.route('/strains', methods=['GET'])
def strains():
    strains = Strain.query.all()
    stores = Store.query.all()
    add_strain_form = AddStrainForm()
    update_strain_form = UpdateStrainForm()
    delete_strain_form = DeleteStrainForm()
    add_strain_form.related_stores.choices = [(store.id, store.name) for store in stores]
    update_strain_form.related_stores.choices = [(store.id, store.name) for store in stores]
    return render_template('strains.html', strains=strains,
                           add_strain_form=add_strain_form,
                           update_strain_form=update_strain_form,
                           delete_strain_form=delete_strain_form,
                           current_user=current_user, stores=stores)
