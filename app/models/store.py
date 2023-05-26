#!/usr/bin/python3
"""Store Model"""
from sqlalchemy import Column, String, ForeignKey
from app import db
from .base import BaseModel

class Store(BaseModel):
    __tablename__ = "stores"
    name = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)
    operating_hours = Column(String(128), nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    owner = db.relationship("User", back_populates="stores")
    strains = db.relationship("Strain", secondary="strain_store", back_populates="stores")

    def add_strain(self, strain_obj):
        """Add a strain to the store"""
        if strain_obj not in self.strains:
            self.strains.append(strain_obj)
