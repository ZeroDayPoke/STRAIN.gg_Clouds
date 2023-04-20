#!/usr/bin/python3
"""Base Model Module"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        
        # Set default values for id, created_at, and updated_at
        kwargs.setdefault('id', str(uuid4()))
        kwargs.setdefault('created_at', datetime.utcnow())
        kwargs.setdefault('updated_at', datetime.utcnow())

        # Set instance attributes
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates the instance in the storage"""
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance, excluding _sa_instance_state"""
        result = self.__dict__.copy()
        result.pop('_sa_instance_state', None)
        result['__class__'] = self.__class__.__name__

        # Convert non-string values to string
        for key, value in result.items():
            if not isinstance(value, str):
                result[key] = str(value)

        return result

    def delete(self):
        """Deletes the instance from the storage"""
        models.storage.delete(self)
