import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class RoleBase(BaseModel):
    name: str
    permissions: Optional[int] = 0

    @staticmethod
    def from_model(entity):
        return RoleBase(
            name=entity.name,
            permissions=entity.permissions
        )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str]
    permissions: Optional[int]


class Role(RoleBase):
    id: int

    @staticmethod
    def from_model(entity):
        return Role(
            id=entity.id,
            name=entity.name,
            permissions=entity.permissions
        )

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    display_name: Optional[str] = None

    @staticmethod
    def from_model(entity):
        return UserBase(
            username=entity.username,
            display_name=entity.display_name
        )


class UserCreate(UserBase):
    password: str

    @validator('username')
    def username_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Username is empty")
        return v

    @validator('password')
    def password_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Password is empty")
        return v


class UserUpdate(BaseModel):
    display_name: Optional[str]
    password: Optional[str]


class User(UserBase):
    id: int
    is_active: bool

    @staticmethod
    def from_model(entity):
        return User(
            username=entity.username,
            display_name=entity.display_name,
            id=entity.id,
            is_active=entity.is_active
        )

    class Config:
        orm_mode = True


class UserDetail(User):
    joined: Optional[datetime.datetime] = None
    modified: Optional[datetime.datetime] = None
    last_active: Optional[datetime.datetime] = None

    @staticmethod
    def from_model(entity):
        return UserDetail(
            username=entity.username,
            display_name=entity.display_name,
            id=entity.id,
            is_active=entity.is_active,
            joined=entity.joined,
            modified=entity.modified,
            last_active=entity.last_active
        )


class UserLogin(BaseModel):
    id: int
    username: str
    password: str

    @staticmethod
    def from_model(entity):
        return UserLogin(
            username=entity.username,
            id=entity.id,
            password=entity.hashed_passcode
        )

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
