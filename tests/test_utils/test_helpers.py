#!/usr/bin/env python3
"""Helpers Testing Module"""
import json
import pytest
from flask import Flask, request
from app.utils.helpers import get_json

@pytest.fixture
def app():
    """ """
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    """ """
    return app.test_client()

def test_get_json_no_required_fields(app):
    """ """
    with app.test_request_context('/path', json={'key': 'value'}):
        result = get_json()
        assert result == {'key': 'value'}

def test_get_json_with_required_fields(app):
    """ """
    with app.test_request_context('/path', json={'key1': 'value1', 'key2': 'value2'}):
        result = get_json(['key1', 'key2'])
        assert result == {'key1': 'value1', 'key2': 'value2'}

def test_get_json_missing_required_fields(app):
    """ """
    with app.test_request_context('/path', json={'key1': 'value1'}):
        with pytest.raises(Exception) as excinfo:
            get_json(['key1', 'key2'])
        assert str(excinfo.value) == '400 Bad Request: Missing key2'
