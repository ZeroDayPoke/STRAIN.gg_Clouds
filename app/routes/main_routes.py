#!/usr/bin/env python3
"""Main Routes for the Flask application"""
# app/routes/main_routes.py
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from ..models import User, Store, Strain
from ..forms import StrainFilterForm

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

@main_routes.route('/stores', methods=['GET', 'POST'])
def stores():
    stores = Store.query.all()
    return render_template('stores.html', stores=stores)

@main_routes.route('/strains', methods=['GET', 'POST'])
def strains():
    form = StrainFilterForm(request.form)
    form.strains.choices = [(str(strain.id), strain.name) for strain in Strain.query.all()]
    if request.method == 'POST' and form.validate():
        selected_strains = form.strains.data
        strains = Strain.query.filter(Strain.id.in_(selected_strains)).all()
    else:
        strains = Strain.query.all()
    return render_template('strains.html', strains=strains, form=form)
