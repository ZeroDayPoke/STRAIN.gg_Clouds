import pytest
from flask import current_app
from app import create_app
from app.config import Config
from app.routes import web_routes, app_routes

@pytest.fixture(scope="module")
def test_client():
    app = create_app(Config)
    testing_client = app.test_client()

    # Establish application context
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

def test_app_creation(test_client):
    assert current_app is not None
    assert current_app.config["SECRET_KEY"] == Config.SECRET_KEY

def test_index_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 404

def test_clouds_route(test_client):
    response = test_client.get("/clouds")
    assert response.status_code == 200
