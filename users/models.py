from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from database import Base


class User(Base):
    __tablename__ = "kolomon_user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    permissions = Column(Integer, default=0)

    joined = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
