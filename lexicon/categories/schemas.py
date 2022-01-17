from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]


class CategoryPatch(CategoryBase):
    name: Optional[str]


class Category(CategoryBase):
    id: str

    class Config:
        orm_mode = True
