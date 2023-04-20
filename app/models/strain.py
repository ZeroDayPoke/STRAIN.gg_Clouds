#!/usr/bin/python3
from sqlalchemy import Column, String, Float
from models.base import BaseModel

class Strain(BaseModel):
    __tablename__ = 'strains'
    name = Column(String(128), nullable=False)
    terpene_profile = Column(String(256), nullable=True)
    delta_nine_concentration = Column(Float, nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
