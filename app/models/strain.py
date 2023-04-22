#!/usr/bin/python3
"""Strain model"""
from sqlalchemy import Column, String, Float
from .base import BaseModel
from sqlalchemy.orm import relationship

class Strain(BaseModel):
    __tablename__ = "strains"
    name = Column(String(128), nullable=False)
    delta_nine_concentration = Column(Float, nullable=True)
    target_symptom = Column(String(128), nullable=True)
    image_filename = Column(String(128), nullable=True)
    users = relationship("User", secondary="user_strain_association", back_populates="favorite_strains")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
