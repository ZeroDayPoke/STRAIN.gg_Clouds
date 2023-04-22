#!/usr/bin/python3
"""Routes for the app"""
import os
from flask import Blueprint, jsonify, request, abort
from ..models import storage, strain, user
from ..utils.helpers import get_json
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

# Blueprint for the app
app_routes = Blueprint('app_routes', __name__, url_prefix='/clouds')

# Constants
UPLOAD_FOLDER = 'app/static/images/strain_images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function
def validate_model(model, model_id):
    """Validate if a model exists"""
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_user():
    return current_user

"""Strain routes"""

@app_routes.route('/api/strains', methods=['GET'], strict_slashes=False)
def get_strains():
    strains = storage.all('Strain')
    return jsonify([strain.to_dict() for strain in strains.values()])


from flask import request
from werkzeug.exceptions import BadRequest

@app_routes.route('/api/strains', methods=['POST'], strict_slashes=False)
def create_strain():
    image = request.files.get('image')
    
    # Set a maximum file size (e.g., 2 MB)
    max_file_size = 1.5 * 1024 * 1024
    
    if image:
        if allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)

            # Check the file size after saving it to the server
            file_size = os.path.getsize(image_path)

            if file_size <= max_file_size:
                new_strain = strain.Strain(name=request.form['name'], delta_nine_concentration=request.form['delta_nine_concentration'], target_symptom=request.form['target_symptom'], image_filename=filename)
            else:
                # Remove the saved file if the size is too large
                os.remove(image_path)
                return jsonify({"success": False, "message": "File size is too large. Maximum allowed file size is 1.5 MB."}), 400
        else:
            return jsonify({"success": False, "message": "Invalid file type."}), 400
    else:
        new_strain = strain.Strain(name=request.form['name'], delta_nine_concentration=request.form['delta_nine_concentration'], target_symptom=request.form['target_symptom'])

    new_strain.save(storage)
    return jsonify({"success": True, "strain": new_strain.to_dict()}), 201


@app_routes.route('/api/strains/<strain_id>', methods=['PUT'], strict_slashes=False)
def update_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)

    image = request.files.get('image')
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        target_strain.image_filename = filename

    try:
        target_strain.name = request.form['name']
        target_strain.delta_nine_concentration = request.form['delta_nine_concentration']
        target_strain.target_symptom = request.form['target_symptom']
        target_strain.save(storage)
        return jsonify({"success": True, "strain": target_strain.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app_routes.route('/api/strains/<strain_id>', methods=['DELETE'], strict_slashes=False)
def delete_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)
    storage.delete(target_strain)
    storage.save()
    return jsonify({"success": True}), 200


@app_routes.route('/api/strains/<strain_id>', methods=['GET'], strict_slashes=False)
def get_strain(strain_id):
    target_strain = validate_model('Strain', strain_id)
    return jsonify({"success": True, "strain": target_strain.to_dict()})


@app_routes.route('/api/favorite_strains/<strain_id>', methods=['POST'], strict_slashes=False)
def create_favorite_strain(strain_id):
    current_user = get_current_user()
    target_strain = validate_model('Strain', strain_id)

    try:
        current_user.add_favorite_strain(target_strain)
        current_user.save(storage)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
