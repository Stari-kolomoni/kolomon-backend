from fastapi import APIRouter
from typing import List

from core.schemas.users_schema import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[User], status_code=200)
async def read_users():
    pass


@router.post("/", response_model=UserDetail, status_code=201,
             responses={400: {}})
async def create_user():
    pass


@router.get("/{user_id}", response_model=UserDetail, status_code=200,
            responses={404: {}})
async def read_user_details(user_id: int):
    pass


@router.patch("/{user_id}", response_model=UserDetail, status_code=200,
              responses={404: {}, 400: {}})
async def update_user(user_id: int):
    pass


@router.delete("/{user_id}", status_code=200,
               responses={404: {}})
async def remove_user(user_id: int):
    pass
