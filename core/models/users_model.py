from sqlalchemy import (Column, Integer, String, DateTime,
                        func, Boolean, SmallInteger, ForeignKey)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    hashed_passcode = Column(String)
    joined = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_onupdate=func.now(), nullable=True)
    last_active = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=False)

    roles = relationship('Role', secondary='role_to_user',
                         back_populates='users')


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    permissions = Column(Integer)
    users = relationship('User', secondary='role_to_user',
                         back_populates='roles')


class RoleToUser(Base):
    __tablename__ = "role_to_user"

    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
