import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    name: str
    permissions: Optional[int] = 0


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    display_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(alias='hashed_passcode')
    roles: List[int] = []


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserDetail(User):
    joined: datetime.datetime
    modified: datetime.datetime
    last_active: datetime.datetime
