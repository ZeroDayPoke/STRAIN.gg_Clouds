#!/usr/bin/env python3
"""User Model"""

# Import necessary modules
from models.base import BaseModel
from sqlalchemy import Column, Integer, String
import hashlib

# Create the User class
class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

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
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexdigest()
        setattr(self, "password", secure_password)
