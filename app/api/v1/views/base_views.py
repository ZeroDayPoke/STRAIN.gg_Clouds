#!/usr/bin/python3
"""API routes for base"""
from flask import Blueprint, jsonify, current_app
from app.models.strain import Strain
from app.models.store import Store
from app.models.user import User

storage = current_app.storage

base_views = Blueprint('base_views', __name__, url_prefix='/api/v1')

@base_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@base_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Strain, Store, User]
    names = ["Strain", "Store", "User"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
