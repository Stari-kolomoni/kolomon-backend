from fastapi import APIRouter, Depends, HTTPException

import core.schemas.message_types as mt
from core.models.database import async_session
from v1.lex.search_dal import SearchDAL

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


async def get_search_dal():
    async with async_session() as session:
        async with session.begin():
            yield SearchDAL(session)


@router.get("/search/entry/simple", status_code=200,
            responses={500: {"model": mt.Message}})
async def simple_search_entries(query: str = "", offset: int = None, limit: int = None, language: str = None,
                                db: SearchDAL = Depends(get_search_dal)):
    filters = {
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.entry_simple_search(query, filters, language)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/search/entry/full", status_code=200,
            responses={500: {"model": mt.Message}})
async def full_search_entries(query: str = "", offset: int = None, limit: int = None, language: str = None,
                              db: SearchDAL = Depends(get_search_dal)):
    filters = {
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.entry_full_search(query, filters, language)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
