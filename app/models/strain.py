#!/usr/bin/python3
"""Strain model"""
from sqlalchemy import Column, String, Float
from .base import BaseModel, Base
from app import db

class Strain(BaseModel):
    __tablename__ = "strains"
    image_filename = Column(String(128), nullable=True)
    name = Column(String(128), nullable=False)
    type = Column(String(128), nullable=True)
    delta_nine_concentration = Column(Float, nullable=True)
    cbd_concentration = Column(Float, nullable=True)
    terpene_profile = Column(String(128), nullable=True)
    effects = Column(String(128), nullable=True)
    uses = Column(String(128), nullable=True)
    flavor = Column(String(128), nullable=True)
    users = db.relationship("User", secondary="user_strain_association", back_populates="favorite_strains")
    stores = db.relationship("Store", secondary="strain_store", back_populates="strains")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
