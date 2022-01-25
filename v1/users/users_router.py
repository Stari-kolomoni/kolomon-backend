from fastapi import APIRouter, Depends, Request
from typing import List

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from core.exceptions import GeneralBackendException
import core.message_types as mt
from core.models.database import async_session
from core.schemas.users_schema import *

import v1.doc_strings as doc_str
from v1.users.users_dal import UserDAL

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)


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
    new_user = await db.create_user(user)
    if new_user is None:
        raise GeneralBackendException(400, "Username already taken")
    return new_user


@router.get("/{user_id}", response_model=UserDetail, status_code=200,
            responses={404: {}}, description=doc_str.GET_USER)
async def read_user_details(user_id: int, db: UserDAL = Depends(get_user_dal)):
    user = await db.get_user(user_id)
    if not user:
        raise GeneralBackendException(404, "User not found")
    return user


@router.put("/{user_id}", response_model=mt.Message, status_code=200,
            responses={404: {}, 400: {}}, description=doc_str.PUT_USER)
async def update_user(user_data: UserUpdate, user_id: int, db: UserDAL = Depends(get_user_dal)):
    updated, msg = await db.update_user(user_data, user_id)
    if not updated:
        raise GeneralBackendException(404, msg)
    return mt.Message(message=msg)


@router.delete("/{user_id}", status_code=200,
               responses={404: {}}, description=doc_str.DELETE_USER)
async def remove_user(user_id: int, db: UserDAL = Depends(get_user_dal)):
    deleted = await db.delete_user(user_id)
    if not deleted:
        raise GeneralBackendException(404, "User not found")
    return mt.Message(message="User deleted")


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
    return mt.Message(message=msg)


@router.delete("/{user_id}/roles", response_model=mt.Message, status_code=200,
               description=doc_str.DELETE_USER_ROLES)
async def remove_user_roles(user_id: int, role_ids: List[int], db: UserDAL = Depends(get_user_dal)):
    removed, msg = await db.remove_user_roles(user_id, role_ids)
    if not removed:
        raise GeneralBackendException(404, msg)
    return mt.Message(message=msg)