#!/usr/bin/python3
"""API utilities"""
import os
from flask import abort
from werkzeug.utils import secure_filename


def allowed_file(filename, allowed_extensions):
    """Check if the file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


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
                    abort(400, {
                          "success": False, "message": f"File size is too large. Maximum allowed file size is {max_size / 1024 / 1024} MB."})
        else:
            abort(400, {
                  "success": False, "message": f"Invalid file type. Allowed file types are {', '.join(allowed_extensions)}."})

        return filename

    return None
