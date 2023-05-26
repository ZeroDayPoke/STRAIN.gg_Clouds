#!/usr/bin/python3
"""Strain routes"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required
from app.models.strain import Strain
from .utils import validate_model, handle_file_upload, format_json_response, ALLOWED_EXTENSIONS
from sqlalchemy.orm import joinedload
from app.models.user import User

strain_views = Blueprint('strain_views', __name__, url_prefix='/clouds/api/v1/strains')

STRAIN_UPLOAD_FOLDER = 'app/static/images/strain_images/'

@strain_views.route('/', methods=['GET'], strict_slashes=False)
def get_strains():
    """api route to get all strains"""
    strains = current_app.storage.all(Strain)
    return jsonify([strain.to_dict() for strain in strains])

@strain_views.route('/', methods=['POST'], strict_slashes=False)
def create_strain():
    """api route to create a strain"""
    image_filename = handle_file_upload(request, STRAIN_UPLOAD_FOLDER, ALLOWED_EXTENSIONS, max_size=1.5 * 1024 * 1024)
    new_strain = Strain(
        name=request.form['name'],
        type=request.form['type'],
        delta_nine_concentration=request.form['delta_nine_concentration'],
        cbd_concentration=request.form['cbd_concentration'],
        terpene_profile=request.form['terpene_profile'],
        effects=request.form['effects'],
        uses=request.form['uses'],
        flavor=request.form['flavor'],
        image_filename=image_filename
    )
    new_strain.save(current_app.storage)
    return jsonify({"success": True, "strain": new_strain.to_dict()}), 201

@strain_views.route('/<strain_id>', methods=['PUT'], strict_slashes=False)
def update_strain(strain_id):
    """api route to update a strain"""
    target_strain = validate_model(Strain, strain_id)
    image_filename = handle_file_upload(request, STRAIN_UPLOAD_FOLDER, ALLOWED_EXTENSIONS)

    if image_filename:
        target_strain.image_filename = image_filename

    target_strain.name = request.form['name']
    target_strain.type = request.form['type']
    target_strain.delta_nine_concentration = request.form['delta_nine_concentration']
    target_strain.cbd_concentration = request.form['cbd_concentration']
    target_strain.terpene_profile = request.form['terpene_profile']
    target_strain.effects = request.form['effects']
    target_strain.uses = request.form['uses']
    target_strain.flavor = request.form['flavor']
    target_strain.save(current_app.storage)
    return jsonify({"success": True, "strain": target_strain.to_dict()}), 200

@strain_views.route('/<strain_id>', methods=['DELETE'], strict_slashes=False)
def delete_strain(strain_id):
    """api route to delete a strain"""
    target_strain = validate_model(Strain, strain_id)
    current_app.storage.delete(target_strain)
    current_app.storage.save()
    return jsonify({"success": True}), 200

@strain_views.route('/<strain_id>', methods=['GET'], strict_slashes=False)
def get_strain(strain_id):
    """api route to get a strain"""
    target_strain = validate_model(Strain, strain_id)
    return jsonify({"success": True, "strain": target_strain.to_dict()})

@strain_views.route('/favorite_strains/<strain_id>', methods=['POST'], strict_slashes=False)
@login_required
def create_favorite_strain(strain_id):
    """API route to add a strain to favorites"""
    # Query for the current user within the session
    user = current_app.storage.session.query(User)\
        .options(joinedload(User.favorite_strains))\
        .filter_by(id=current_user.id)\
        .one()

    target_strain = validate_model(Strain, strain_id)

    if target_strain is None:
        return jsonify({"success": False, "message": "Invalid strain ID"}), 404

    try:
        user.add_favorite_strain(target_strain)
        current_app.storage.session.commit()  # commit the transaction
        return jsonify({"success": True, "strain": target_strain.to_dict()}), 201
    except Exception as e:
        current_app.storage.session.rollback()  # rollback the transaction in case of error
        return jsonify({"success": False, "message": str(e)}), 400
