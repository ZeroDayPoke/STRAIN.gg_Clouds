# This file contains the helper functions for the app
from flask import abort, request

# Helper functions

def validate_model(model, model_id):
    """Validate if a model exists"""
    from models import storage
    obj = storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj

def get_json(required_fields=[]):
    """Get the json from the request"""
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for field in required_fields:
        if result.get(field) is None:
            abort(400, 'Missing {}'.format(field))
    return result