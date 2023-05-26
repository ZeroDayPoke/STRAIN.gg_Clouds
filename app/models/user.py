#!/usr/bin/env python3
"""User Model"""

# Import necessary modules
from .base import BaseModel, Base
from sqlalchemy import Column, Integer, String, Enum
from app import db
from sqlalchemy_utils import ChoiceType
from werkzeug.security import generate_password_hash

# Define the UserRole enumeration
class UserRole(Enum):
    CLOUD_GUEST = 'CLOUD_GUEST'
    CLOUD_CONSUMER = 'CLOUD_CONSUMER'
    CLOUD_PRODUCER = 'CLOUD_PRODUCER'
    CLOUD_VENDOR = 'CLOUD_VENDOR'
    CLOUD_CHASER = 'CLOUD_CHASER'

# Create the User class
class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(ChoiceType(UserRole, impl=String(20)), default=UserRole.CLOUD_CONSUMER, nullable=False)
    favorite_strains = db.relationship("Strain", secondary="user_strain_association", back_populates="users")
    stores = db.relationship("Store", back_populates="owner")

    def __init__(self, *args, **kwargs):
        """creates new User"""
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        else:
            kwargs['role'] = UserRole.CLOUD_CONSUMER

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
