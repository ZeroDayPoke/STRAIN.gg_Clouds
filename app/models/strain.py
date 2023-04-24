#!/usr/bin/python3
"""Strain model"""
from sqlalchemy import Column, String, Float, ForeignKey, Table
from .base import BaseModel, Base
from sqlalchemy.orm import relationship

strain_store = Table('strain_store', Base.metadata,
                     Column('strain_id', String(60), ForeignKey('strains.id'), primary_key=True),
                     Column('store_id', String(60), ForeignKey('stores.id'), primary_key=True))


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
    users = relationship("User", secondary="user_strain_association", back_populates="favorite_strains")
    stores = relationship("Store", secondary=strain_store, back_populates="strains")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
