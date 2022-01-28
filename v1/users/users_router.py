from datetime import timedelta

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse

from core import settings
from core.exceptions import GeneralBackendException
import core.message_types as mt
from core.models.database import async_session
from core.schemas.users_schema import *

import v1.doc_strings as doc_str
from v1.dependencies import oauth2_scheme
from v1.users.users_dal import UserDAL

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=['bcrypt'])


async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


async def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        print("PWD error")
        return False


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db: UserDAL):
    user = await db.get_user_credentials_by_username(username)
    if (not user or
            not await verify_password(password, user.password)):
        return False
    return user


async def get_current_user(db: UserDAL = Depends(get_user_dal),
                           token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.get("/", response_model=List[User], status_code=200,
            description=doc_str.GET_USERS)
async def read_users(req: Request, db: UserDAL = Depends(get_user_dal)):
    params = req.query_params

    content, count = await db.get_users(params)
    json_content = jsonable_encoder(content)
    headers = {"X-Total-Count": str(count)}
    return JSONResponse(
        content=json_content, headers=headers
    )


@router.post("/", response_model=UserDetail, status_code=201,
             responses={400: {}}, description=doc_str.POST_USER)
async def create_user(user: UserCreate, db: UserDAL = Depends(get_user_dal)):
    user.password = await get_password_hash(user.password)
    new_user = await db.create_user(user)
    if new_user is None:
        raise GeneralBackendException(400, "Username already taken")
    return new_user


@router.get("/me", response_model=UserDetail)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/perms")
async def read_user_me_roles(current_user: User = Depends(get_current_user),
                             db: UserDAL = Depends(get_user_dal)):
    roles = await db.get_user_roles_by_username(current_user.username)
    perms = 0
    for role in roles:
        perms = perms | role.permissions
    return {
        'permissions': perms
    }


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: UserDAL = Depends(get_user_dal)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.get("/{user_id}", response_model=UserDetail, status_code=200,
            responses={404: {}}, description=doc_str.GET_USER)
async def read_user_details(user_id: int, db: UserDAL = Depends(get_user_dal)):
    user = await db.get_user(user_id)
    if not user:
        raise GeneralBackendException(404, "User not found")
    return user


@router.put("/{user_id}", response_model=mt.Message, status_code=200,
            responses={404: {}, 400: {}}, description=doc_str.PUT_USER)
async def update_user(user_data: UserUpdate, user_id: int, db: UserDAL = Depends(get_user_dal),
                      current_user: UserDetail = Depends(get_current_user)):
    if user_id != current_user.id:
        raise GeneralBackendException(401, "You are not the owner of this account.")
    updated, msg = await db.update_user(user_data, user_id)
    if not updated:
        raise GeneralBackendException(404, msg)
    return mt.Message(detail=msg)


@router.delete("/{user_id}", status_code=200,
               responses={404: {}}, description=doc_str.DELETE_USER)
async def remove_user(user_id: int, db: UserDAL = Depends(get_user_dal)):
    deleted = await db.delete_user(user_id)
    if not deleted:
        raise GeneralBackendException(404, "User not found")
    return mt.Message(detail="User deleted")


@router.get("/{user_id}/roles", response_model=List[Role], status_code=200,
            description=doc_str.GET_USER_ROLES)
async def read_user_roles(req: Request, user_id: int, db: UserDAL = Depends(get_user_dal)):
    params = req.query_params
    content, count = await db.get_user_roles(user_id, params)
    json_content = jsonable_encoder(content)
    headers = {"X-Total-Count": str(count)}
    return JSONResponse(
        content=json_content, headers=headers
    )


@router.post("/{user_id}/roles", response_model=mt.Message, status_code=200,
             description=doc_str.POST_USER_ROLES)
async def add_user_roles(user_id: int, role_ids: List[int], db: UserDAL = Depends(get_user_dal)):
    added, msg = await db.create_user_roles(user_id, role_ids)
    if not added:
        raise GeneralBackendException(404, msg)
    return mt.Message(detail=msg)


@router.delete("/{user_id}/roles", response_model=mt.Message, status_code=200,
               description=doc_str.DELETE_USER_ROLES)
async def remove_user_roles(user_id: int, role_ids: List[int], db: UserDAL = Depends(get_user_dal)):
    removed, msg = await db.remove_user_roles(user_id, role_ids)
    if not removed:
        raise GeneralBackendException(404, msg)
    return mt.Message(detail=msg)
