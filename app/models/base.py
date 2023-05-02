#!/usr/bin/python3
"""Base Model"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base, Mapped
from typing import Dict, List
from flask import current_app
from dateutil.parser import parse

Base = declarative_base()

class BaseModel(Base):
    """Abstract base class for all database models.

    This class provides basic functionality for creating, retrieving, updating,
    and deleting instances of database models. Subclasses should define their
    own properties and methods as needed.

    Attributes:
        id (str): The unique identifier of the instance.
        created_at (datetime): The date and time the instance was created.
        updated_at (datetime): The date and time the instance was last updated.

    """
    __abstract__ = True
    id: Mapped[str] = Column(String(60), primary_key=True, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)


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

    @property
    def prop_id(self) -> str:
        return self.id

    @property
    def prop_created_at(self) -> datetime:
        return self.created_at

    @property
    def prop_updated_at(self) -> datetime:
        return self.updated_at

    def create(self):
        """Create a new instance in the database."""
        current_app.storage.new(self)
        current_app.storage.save()

    @classmethod
    def get(cls, id: str) -> 'BaseModel':
        """Retrieve an instance by ID."""
        return current_app.storage.get(cls, id)

    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary representation of the instance.

        The dictionary should exclude the '_sa_instance_state' attribute.

        Returns:
            A dictionary containing the instance's attributes.

        """
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        result.pop('_sa_instance_state', None)
        result['__class__'] = self.__class__.__name__
        for key, value in result.items():
            if not isinstance(value, str):
                result[key] = str(value)
        return result

    def delete(self):
        """Delete the instance from the database."""
        current_app.storage.delete(self)
        current_app.storage.save()

    @classmethod
    def count(cls) -> int:
        """Count the number of instances of this model in the database."""
        return current_app.storage.count(cls)

    @classmethod
    def delete_all(cls):
        """Delete all instances of this model from the database."""
        current_app.storage.delete_all(cls)
        current_app.storage.save()

    @classmethod
    def all(cls) -> List['BaseModel']:
        """Return a list of all instances of this model."""
        return current_app.storage.all(cls)

    @classmethod
    def search(cls, **kwargs) -> List['BaseModel']:
        """Search for instances of this model that match the provided criteria.

        Args:
            **kwargs: The attribute values to match.

        Returns:
            A list of instances of this model that match the provided criteria.

        """
        matches = []
        for instance in cls.all():
            is_match = True
            for attr, val in kwargs.items():
                if not hasattr(instance, attr) or getattr(instance, attr) != val:
                    is_match = False
                    break
            if is_match:
                matches.append(instance)
        return matches

    def save(self):
        """Save the instance to the database.

        If the instance already exists, update it; otherwise, create a new instance.
        """
        existing_instance = self.get(self.id)
        if existing_instance:
            print(f"Existing instance found: {existing_instance.to_dict()}")
            instance_dict = self.to_dict()
            instance_dict.pop('__class__', None)  # Remove the __class__ key
            self.update(**instance_dict)  # Pass the modified dictionary
        else:
            print(f"Creating new instance: {self.to_dict()}")
            self.create()

    def update(self, **kwargs):
        """Update the instance's attributes and save the changes to the database."""
        for attr, val in kwargs.items():
            if hasattr(self, attr) and attr not in ['created_at', '__class__']:
                current_value = getattr(self, attr)
                if isinstance(current_value, datetime) and isinstance(val, str):
                    val = parse(val)
                if val is not None and current_value != val:
                    print(f"Updating {attr} from {current_value} to {val}")
                    setattr(self, attr, val)
        self.updated_at = datetime.utcnow()
        current_app.storage.new(self)
        current_app.storage.save()
