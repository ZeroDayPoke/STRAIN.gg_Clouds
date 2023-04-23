#!/usr/bin/python3
"""Store Model"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Store(BaseModel):
    __tablename__ = "stores"
    name = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)
    operating_hours = Column(String(128), nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="stores")
    strains = relationship("Strain", secondary="strain_store", back_populates="stores")
