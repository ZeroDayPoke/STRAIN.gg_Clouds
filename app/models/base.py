#!/usr/bin/python3
"""Base Model"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base, Mapped
from typing import Dict, List
from app import db  # import the db instance from the app package
from dateutil.parser import parse

Base = declarative_base()

class BaseModel(Base):
    """Abstract base class for all database models."""
    __abstract__ = True
    id: Mapped[str] = Column(String(60), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
