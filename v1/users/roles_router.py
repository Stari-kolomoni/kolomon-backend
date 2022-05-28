from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from core.exceptions import GeneralBackendException
import core.schemas.message_types as mt
from core.models.database import async_session
from core.schemas.users_schema import Role, RoleCreate, RoleUpdate

import v1.doc_strings as doc_str
from v1.users.roles_dal import RoleDAL

router = APIRouter(
    prefix="/roles",
    tags=["Users"]
)


async def get_role_dal():
    async with async_session() as session:
        async with session.begin():
            yield RoleDAL(session)


@router.get("/", response_model=list[Role], status_code=200,
            description=doc_str.GET_ROLES)
async def read_all_roles(req: Request, db: RoleDAL = Depends(get_role_dal)):
    params = req.query_params

    content, count = await db.get_roles(params)
    json_content = jsonable_encoder(content)
    headers = {"X-Total-Count": str(count)}
    return JSONResponse(
        content=json_content, headers=headers
    )


@router.post("/", response_model=Role, status_code=201,
             responses={400: {}}, description=doc_str.POST_ROLE)
async def create_role(role: RoleCreate, db: RoleDAL = Depends(get_role_dal)):
    new_role = await db.create_role(role)
    if new_role is None:
        raise GeneralBackendException(400, "Error creating Role")
    return new_role


@router.get("/{role_id}", response_model=Role, status_code=200,
            responses={404: {'model': mt.Message}}, description=doc_str.GET_ROLE)
async def read_role(role_id: int, db: RoleDAL = Depends(get_role_dal)):
    role = await db.get_role(role_id)
    if not role:
        raise GeneralBackendException(404, "Role not found")
    return role


@router.put("/{role_id}", response_model=mt.Message, status_code=200,
            responses={404: {'model': mt.Message}}, description=doc_str.PUT_ROLE)
async def update_role(role_data: RoleUpdate, role_id: int, db: RoleDAL = Depends(get_role_dal)):
    updated, msg = await db.update_role(role_data, role_id)
    if not updated:
        raise GeneralBackendException(404, "Role not found")
    return mt.Message(detail=msg)


@router.delete("/{role_id}", response_model=mt.Message, status_code=200,
               responses={404: {'model': mt.Message}}, description=doc_str.DELETE_ROLE)
async def remove_role(role_id: int, db: RoleDAL = Depends(get_role_dal)):
    deleted = await db.delete_role(role_id)
    if not deleted:
        raise GeneralBackendException(404, "Role not found")
    return mt.Message(detail="Role deleted")
