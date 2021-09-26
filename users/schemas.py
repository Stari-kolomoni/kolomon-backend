from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    permissions: Optional[int] = 0


class UserPatch(BaseModel):
    password: Optional[str]
    permissions: Optional[int]


class User(UserBase):
    id: int
    permissions: int
    joined: datetime
    last_active: datetime
    is_active: bool

    class Config:
        orm_mode = True
