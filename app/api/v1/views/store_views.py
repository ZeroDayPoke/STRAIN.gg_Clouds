#!/usr/bin/python3
"""Store routes"""
from flask import Blueprint, jsonify, request, current_app
from app.models.store import Store
from utils import validate_model, handle_file_upload, ALLOWED_EXTENSIONS

app_routes = Blueprint('app_routes', __name__, url_prefix='/api/v1/stores')

STORES_UPLOAD_FOLDER = 'app/static/images/store_images/'

@app_routes.route('/', methods=['GET'], strict_slashes=False)
def get_stores():
    """api route to get all stores"""
    stores = current_app.storage.all('Store')
    return jsonify([store.to_dict() for store in stores.values()])

@app_routes.route('/', methods=['POST'], strict_slashes=False)
def create_store():
    """api route to create a store"""
    image_filename = handle_file_upload(request, STORES_UPLOAD_FOLDER, ALLOWED_EXTENSIONS)
    new_store = Store(
        name=request.form['name'],
        location=request.form['location'],
        operating_hours=request.form['operating_hours'],
        owner_id=request.form['owner_id'],
        image_filename=image_filename
    )
    new_store.save(current_app.storage)
    return jsonify({"success": True, "store": new_store.to_dict()}), 201

@app_routes.route('/<store_id>', methods=['PUT'], strict_slashes=False)
def update_store(store_id):
    """api route to update a store"""
    target_store = validate_model('Store', store_id)

    target_store.name = request.form['name']
    target_store.location = request.form['location']
    target_store.operating_hours = request.form['operating_hours']
    target_store.save(current_app.storage)
    return jsonify({"success": True, "store": target_store.to_dict()}), 200

@app_routes.route('/<store_id>', methods=['DELETE'], strict_slashes=False)
def delete_store(store_id):
    """api route to delete a store"""
    target_store = validate_model('Store', store_id)
    current_app.storage.delete(target_store)
    current_app.storage.save()
    return jsonify({"success": True}), 200

@app_routes.route('/<store_id>', methods=['GET'], strict_slashes=False)
def get_store(store_id):
    """api route to get a store"""
    target_store = validate_model('Store', store_id)
    return jsonify({"success": True, "store": target_store.to_dict()})

@app_routes.route('/<store_id>/strains', methods=['PUT'], strict_slashes=False)
def add_strain_to_store(store_id):
    """api route to add a strain to a store"""
    target_store = validate_model('Store', store_id)
    strain_id = request.form['strain_id']
    target_strain = validate_model('Strain', strain_id)

    target_store.add_strain(target_strain)
    target_store.save(current_app.storage)
    return jsonify({"success": True, "store": target_store.to_dict()}), 201

@app_routes.route('/<store_id>/strains', methods=['GET'], strict_slashes=False)
def get_strains_in_store(store_id):
    """api route to get all strains in a store"""
    target_store = validate_model('Store', store_id)
    strains_in_store = [strain.to_dict() for strain in target_store.strains]
    return jsonify(strains_in_store)
