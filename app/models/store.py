#!/usr/bin/python3
"""Store Model"""
from .base import BaseModel, db
from .associations import store_strains

class Store(BaseModel):
    __tablename__ = "stores"
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    operating_hours = db.Column(db.String(128), nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship("User", back_populates="stores")
    related_strains = db.relationship("Strain", secondary=store_strains, back_populates="related_stores")

    def add_strain(self, strain_obj):
        """Add a strain to the store"""
        if strain_obj not in self.related_strains:
            self.related_strains.append(strain_obj)

    def __repr__(self):
        return f"<Store (ID: {self.id}, Name: {self.name})>"
