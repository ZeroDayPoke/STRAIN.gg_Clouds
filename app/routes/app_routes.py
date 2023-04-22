#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, jsonify, request, abort
from ..models import storage, strain, user
from ..utils.helpers import get_json

# Blueprint for the app
app_routes = Blueprint('app_routes', __name__, url_prefix='/clouds')

# Helper function
def validate_model(model, model_id):
    """Validate if a model exists"""
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj

"""Strain routes"""

@app_routes.route('/api/strains', methods=['GET'], strict_slashes=False)
def get_strains():
    strains = storage.all('Strain')
    return jsonify([strain.to_dict() for strain in strains.values()])


@app_routes.route('/api/strains', methods=['POST'], strict_slashes=False)
def create_strain():
    data = get_json(['name', 'delta_nine_concentration', 'target_symptom'])
    
    new_strain = strain.Strain(name=data['name'], delta_nine_concentration=data['delta_nine_concentration'], target_symptom=data['target_symptom'])
    new_strain.save(storage)
    return jsonify(new_strain.to_dict()), 201


@app_routes.route('/api/strains/<strain_id>', methods=['PUT'], strict_slashes=False)
def update_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)

    print(target_strain)
    data = get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(target_strain, key, value)
    target_strain.save(storage)
    return jsonify(target_strain.to_dict()), 200


@app_routes.route('/api/strains/<strain_id>', methods=['DELETE'], strict_slashes=False)
def delete_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)
    storage.delete(target_strain)
    storage.save()
    return jsonify({}), 200


@app_routes.route('/api/strains/<strain_id>', methods=['GET'], strict_slashes=False)
def get_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)
    return jsonify(target_strain.to_dict())
