#!/usr/bin/python3

# This file contains the helper functions for the app
from functools import wraps
from flask import abort, request, make_response

# Helper functions

def get_json(required_fields=[]):
    """Get the json from the request"""
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for field in required_fields:
        if result.get(field) is None:
            abort(400, 'Missing {}'.format(field))
    return result

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return no_cache
