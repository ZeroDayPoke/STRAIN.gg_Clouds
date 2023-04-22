#!/usr/bin/env python3
"""User Model"""

# Import necessary modules
from .base import BaseModel, Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from werkzeug.security import generate_password_hash

# Import Enum for Python 3.4 and later
from enum import Enum

# Define the UserRole enumeration
class UserRole(Enum):
    CLOUD_CONSUMER = 'CLOUD_CONSUMER'
    CLOUD_PRODUCER = 'CLOUD_PRODUCER'

# Create the association table for users and their favorite strains
user_strain_association = Table(
    "user_strain_association",
    Base.metadata,
    Column("user_id", String(60), ForeignKey("users.id"), primary_key=True),
    Column("strain_id", String(60), ForeignKey("strains.id"), primary_key=True),
)

# Create the User class
class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(ChoiceType(UserRole, impl=String(20)), default=UserRole.CLOUD_CONSUMER, nullable=False)
    favorite_strains = relationship("Strain", secondary=user_strain_association, back_populates="users")

    def __init__(self, *args, **kwargs):
        """creates new User"""
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """User representation"""
        return f'<User {self.username}>'

    def __set_password(self, pwd):
        """encrypts password"""
        secure_password = generate_password_hash(pwd)
        setattr(self, "password", secure_password)

    @property
    def is_authenticated(self):
        """Checks if user is authenticated"""
        return True

    @property
    def is_active(self):
        """Checks if user is active"""
        return True

    @property
    def is_anonymous(self):
        """Checks if user is anonymous"""
        return False

    def get_id(self):
        """Gets the user id"""
        return str(self.id)

    def add_favorite_strain(self, strain):
        """Adds a strain to the user's favorites"""
        if strain not in self.favorite_strains:
            self.favorite_strains.append(strain)

    def remove_favorite_strain(self, strain):
        """Removes a strain from the user's favorites"""
        if strain in self.favorite_strains:
            self.favorite_strains.remove(strain)
