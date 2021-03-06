from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String, nullable=True)
    hashed_passcode = Column(String)
    joined = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, onupdate=func.now(), nullable=True)
    last_active = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=False)
    roles = relationship("Role", secondary="role_to_user",
                         back_populates="users")

    __mapper__args = {"eager_defaults": True}

    def __str__(self):
        return f"User {self.username}"

    @staticmethod
    def from_schema(entity):
        return User(
            username=entity.username,
            display_name=entity.display_name,
            hashed_passcode=entity.password
        )


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    permissions = Column(Integer)
    users = relationship("User", secondary="role_to_user",
                         back_populates="roles")

    __mapper__args = {"eager_defaults": True}

    @staticmethod
    def from_schema(entity):
        return Role(
            name=entity.name,
            permissions=entity.permissions
        )


class RoleToUser(Base):
    __tablename__ = "role_to_user"

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    __mapper__args = {"eager_defaults": True}
