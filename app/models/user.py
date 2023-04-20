#!/usr/bin/env python3
"""User Model"""

# Import necessary modules
from models.base import BaseModel
from sqlalchemy import Column, Integer, String

# Create the User class
class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
