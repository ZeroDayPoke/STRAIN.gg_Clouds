#!/usr/bin/env python3
"""Strain model"""

from sqlalchemy import Enum
from .base import BaseModel, db
from .associations import user_strains, store_strains

class Strain(BaseModel):
    __tablename__ = "strains"
    image_filename = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(128), nullable=False)
    subtype = db.Column(Enum('Indica', 'Sativa', 'Hybrid', 'Unknown'), nullable=True)
    thc_concentration = db.Column(db.Float, nullable=True)
    cbd_concentration = db.Column(db.Float, nullable=True)
    related_users = db.relationship("User", secondary=user_strains, back_populates="favorite_strains")
    related_stores = db.relationship("Store", secondary=store_strains, back_populates="related_strains")

    def __repr__(self):
        return f"<Strain (ID: {self.id}, Name: {self.name})>"
