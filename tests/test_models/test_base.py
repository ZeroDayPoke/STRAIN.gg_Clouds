#!/usr/bin/python3
"""Base Testing Module"""
import pytest
from datetime import datetime
from app.models.base import BaseModel

class DummyModel(BaseModel):
    """Dummy Base Class"""
    __tablename__ = 'dummy'
    pass

def test_base_model_init():
    """ """
    dummy = DummyModel()

    assert dummy.id is not None
    assert isinstance(dummy.created_at, datetime)
    assert isinstance(dummy.updated_at, datetime)

def test_base_model_save(mocker):
    """ """
    storage_mock = mocker.Mock()
    dummy = DummyModel()

    dummy.save(storage_mock)

    storage_mock.new.assert_called_once_with(dummy)
    storage_mock.save.assert_called_once()

def test_base_model_to_dict():
    """ """
    dummy = DummyModel()
    dummy_dict = dummy.to_dict()

    assert '__class__' in dummy_dict
    assert dummy_dict['__class__'] == 'DummyModel'
    assert '_sa_instance_state' not in dummy_dict
    assert isinstance(dummy_dict['id'], str)
    assert isinstance(dummy_dict['created_at'], str)
    assert isinstance(dummy_dict['updated_at'], str)

def test_base_model_delete(mocker):
    """ """
    storage_mock = mocker.Mock()
    dummy = DummyModel()

    dummy.delete(storage_mock)

    storage_mock.delete.assert_called_once_with(dummy)
