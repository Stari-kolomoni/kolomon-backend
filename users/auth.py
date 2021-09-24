from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dependencies import oauth2_scheme, get_db
from users import models, crud

SECRET_KEY = "750004cfb923c46a8bf40677944222720985541015CC905b5a01940839fodfa5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hash_password) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> Optional[models.User]:
    user = crud.get_user_by_username(db, username)
    if user:
        return user
    return None


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neveljaven vpis",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
