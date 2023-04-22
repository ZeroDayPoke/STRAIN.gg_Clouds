#!/usr/bin/python3

# This file contains the helper functions for the app
from flask import abort, request

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
