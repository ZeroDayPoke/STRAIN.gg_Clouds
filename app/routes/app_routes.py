#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request
from ..models import storage, strain, user

# Blueprint for the app
app_routes = Blueprint('app_routes', __name__)

"""Strain routes"""
@app_routes.route('/app/strains', methods=['GET'], strict_slashes=False)
def get_strains():
    strains = storage.all('Strain')
    return jsonify([strain.to_dict() for strain in strains.values()])
