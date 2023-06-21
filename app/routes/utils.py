#!/usr/bin/python3
"""API utilities"""
import os
from flask import jsonify, abort, current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'}

def allowed_file(filename, allowed_extensions):
    """Check if the file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_model(model, model_id):
    """Validate if a model exists"""
    obj = current_app.storage.get(model, model_id)
    if obj is None:
        abort(404)
    return obj

def handle_file_upload(request, upload_folder, allowed_extensions, max_size=None):
    """Handles file uploads and checks file types and sizes"""
    file = request.files.get('image')

    if file:
        if allowed_file(file.filename, allowed_extensions):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            if max_size is not None:
                file_size = os.path.getsize(file_path)
                if file_size > max_size:
                    os.remove(file_path)
                    abort(400, {"success": False, "message": f"File size is too large. Maximum allowed file size is {max_size / 1024 / 1024} MB."})
        else:
            abort(400, {"success": False, "message": f"Invalid file type. Allowed file types are {', '.join(allowed_extensions)}."})

        return filename

    return None

def format_json_response(data, status=200):
    """Formats a JSON response object with the given data and status code"""
    response = jsonify(data)
    response.status_code = status
    return response
