#!/usr/bin/env python3
"""User Testing Module"""
import pytest
from app.models.user import User, UserRole
from app.models.strain import Strain
from werkzeug.security import check_password_hash

def test_user_init():
    """ """
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        role=UserRole.CLOUD_PRODUCER
    )

    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert check_password_hash(user.password, "test_password")
    assert user.role == UserRole.CLOUD_PRODUCER

def test_user_init_no_args():
    """ """
    user = User()

    assert user.username is None
    assert user.email is None
    assert user.password is None
    assert user.role == UserRole.CLOUD_CONSUMER

def test_user_repr():
    """ """
    user = User(username="test_user")

    assert repr(user) == '<User test_user>'

def test_user_favorite_strains():
    """ """
    user = User()
    strain1 = Strain(name="Test Strain 1")
    strain2 = Strain(name="Test Strain 2")

    # Test adding favorite strains
    user.add_favorite_strain(strain1)
    user.add_favorite_strain(strain2)
    assert len(user.favorite_strains) == 2
    assert strain1 in user.favorite_strains
    assert strain2 in user.favorite_strains

    # Test removing favorite strains
    user.remove_favorite_strain(strain1)
    assert len(user.favorite_strains) == 1
    assert strain1 not in user.favorite_strains
    assert strain2 in user.favorite_strains
