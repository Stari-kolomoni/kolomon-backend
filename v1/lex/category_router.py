from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

import core.schemas.message_types as mt
from core.models.database import async_session
from core.schemas.lex_schema import *
from v1.lex.category_dal import CategoryDAL


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


async def get_category_dal():
    async with async_session() as session:
        async with session.begin():
            yield CategoryDAL(session)


@router.post("/", status_code=201,
             responses={500: {"model": mt.Message}})
async def add_category(category: CategoryCreate, db: CategoryDAL = Depends(get_category_dal)):
    try:
        await db.add_category(category)
        return mt.Message(
            detail="Category successfully added!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/", status_code=200,
            responses={500: {"model": mt.Message}})
async def retrieve_categories(sort: str = "name", offset: int = None, limit: int = None,
                              db: CategoryDAL = Depends(get_category_dal)):
    filters = {
        "sort": sort,
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.retrieve_categories(filters)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{category_id}/entries", status_code=200,
            responses={500: {"model": mt.Message}})
async def retrieve_entries(category_id: int, sort: str = "lemma",
                           offset: int = None, limit: int = None,
                           db: CategoryDAL = Depends(get_category_dal)):
    filters = {
        "sort": sort,
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.retrieve_entries_by_category(filters, category_id)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.put("/{category_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       404: {"model": mt.Message}})
async def update_category(category_id: int, category_update: CategoryCreate,
                          db: CategoryDAL = Depends(get_category_dal)):
    try:
        await db.update_category(category_id, category_update)
        return mt.Message(
            detail="Category successfully changed!"
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.delete("/{category_id}", status_code=200,
               responses={500: {"model": mt.Message}})
async def delete_category(category_id: int, db: CategoryDAL = Depends(get_category_dal)):
    try:
        await db.remove_category(category_id)
        return mt.Message(
            detail="Category successfully deleted!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
