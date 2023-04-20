#!/usr/bin/python3
from sqlalchemy import Column, String, Float
from .base import BaseModel
from sqlalchemy.orm import relationship

class Strain(BaseModel):
    __tablename__ = "strains"
    name = Column(String(128), nullable=False)
    terpene_profile = Column(String(256), nullable=True)
    delta_nine_concentration = Column(Float, nullable=True)
    users = relationship("User", secondary="user_strain_association", back_populates="favorite_strains")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
