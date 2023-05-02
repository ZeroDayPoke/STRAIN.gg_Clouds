#!/usr/bin/python3
"""This module initializes the api routes for the application."""
from flask import Blueprint


api_routes_v1 = Blueprint('api_routes_v1', __name__)


def init_app(app):
    from .store_views import store_views
    from .strain_views import strain_views
    from .user_views import user_views
    from .base_views import base_views

    app.register_blueprint(base_views)
    app.register_blueprint(store_views)
    app.register_blueprint(strain_views)
    app.register_blueprint(user_views)
