from typing import List

from fastapi import APIRouter, Depends, HTTPException

from core.exceptions import GeneralBackendException
import core.message_types as mt
from core.models.database import async_session
from core.schemas.users_schema import Role, RoleCreate, RoleUpdate

from v1.users.roles_dal import RoleDAL

router = APIRouter(
    prefix="/roles",
    tags=["Users"]
)


async def get_role_dal():
    async with async_session() as session:
        async with session.begin():
            yield RoleDAL(session)


@router.get("/", response_model=List[Role], status_code=200)
async def read_roles(db: RoleDAL = Depends(get_role_dal)):
    return await db.get_all_roles()


@router.post("/", response_model=Role, status_code=201,
             responses={400: {}})
async def create_role(role: RoleCreate, db: RoleDAL = Depends(get_role_dal)):
    return await db.create_role(role)


@router.get("/{role_id}", response_model=Role, status_code=200,
            responses={404: {'model': mt.Message}})
async def read_role(role_id: int, db: RoleDAL = Depends(get_role_dal)):
    result = await db.get_role(role_id)
    if not result:
        raise GeneralBackendException(404, "Role not found")
    return result


@router.patch("/{role_id}", response_model=Role, status_code=200,
              responses={404: {}, 400: {}})
async def update_role(role_id: int, role: RoleUpdate):
    pass


@router.delete("/{role_id}", status_code=200,
               responses={404: {}})
async def remove_role(role_id: int):
    pass
