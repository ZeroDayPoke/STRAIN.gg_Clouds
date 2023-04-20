#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request
from models import storage
from models.strain import Strain

# Blueprint for the app
api_routes = Blueprint('api_routes', __name__)

"""Strain routes"""
@api_routes.route('/api/strains', methods=['GET'], strict_slashes=False)
def get_strains():
    strains = storage.all('Strain')
    return jsonify([strain.to_dict() for strain in strains.values()])
