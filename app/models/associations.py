#!/usr/bin/env python3
"""Associations"""
# Path: STRAIN.gg_Clouds/app/models/associations.py
from .base import db

user_strains = db.Table(
    'user_strains',
    db.Column('user_id', db.String(60), db.ForeignKey('users.id'), primary_key=True),
    db.Column('strain_id', db.String(60), db.ForeignKey('strains.id'), primary_key=True)
)

store_strains = db.Table(
    'store_strains',
    db.Column('store_id', db.String(60), db.ForeignKey('stores.id'), primary_key=True),
    db.Column('strain_id', db.String(60), db.ForeignKey('strains.id'), primary_key=True)
)

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.String(60), db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.String(60), db.ForeignKey('roles.id'), primary_key=True)
)
