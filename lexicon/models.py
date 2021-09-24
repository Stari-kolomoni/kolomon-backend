from sqlalchemy import Column, String, Integer
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
