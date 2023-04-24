#!/usr/bin/python3
"""DBStorage Testing Module"""
import os
from dotenv import load_dotenv
import pytest
from app.models import user, strain
from app.models.engine.dbstorage import DBStorage

load_dotenv()

@pytest.fixture(scope='module')
def storage():
    """ """
    storage = DBStorage()
    storage.reload()
    yield storage
    storage.close()

def test_db_storage_instance(storage):
    """ """
    assert isinstance(storage, DBStorage)

def test_all_no_cls(storage):
    """ """
    all_objects = storage.all()
    assert isinstance(all_objects, dict)
    assert all(isinstance(obj, (user.User, strain.Strain)) for obj in all_objects.values())

def test_all_with_cls(storage):
    """ """
    all_users = storage.all('User')
    assert isinstance(all_users, dict)
    assert all(isinstance(obj, user.User) for obj in all_users.values())

def test_new(storage):
    """ """
    new_user = user.User(username='testuser', email='testuser@example.com', password='testpassword')
    storage.new(new_user)
    storage.save()

    fetched_user = storage.get('User', new_user.id)
    assert fetched_user is not None
    assert fetched_user.id == new_user.id

def test_delete(storage):
    """ """
    new_user = user.User(username='testuser2', email='testuser2@example.com', password='testpassword')
    storage.new(new_user)
    storage.save()

    fetched_user = storage.get('User', new_user.id)
    assert fetched_user is not None
    assert fetched_user.id == new_user.id

    storage.delete(fetched_user)
    storage.save()

    fetched_user = storage.get('User', new_user.id)
    assert fetched_user is None

def test_count(storage):
    """ """
    user_count = storage.count('User')
    strain_count = storage.count('Strain')
    total_count = storage.count()

    assert user_count > 0
    assert strain_count > 0
    assert total_count == user_count + strain_count

def test_delete_all(storage):
    """ """
    storage.delete_all('User')
    storage.save()

    all_users = storage.all('User')
    assert len(all_users) == 0
