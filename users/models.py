from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from database import Base


class User(Base):
    __tablename__ = "kolomon_user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    permissions = Column(Integer, default=0)

    joined = Column(DateTime)
    last_active = Column(DateTime)
    is_active = Column(Boolean, default=True)
