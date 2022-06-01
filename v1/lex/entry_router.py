from typing import Union

from fastapi import APIRouter, Depends, HTTPException

import core.schemas.message_types as mt
from core.exceptions import GeneralBackendException
from core.models.database import async_session
from core.schemas.lex_schema import *
from v1 import doc_strings
from v1.lex.entry_dal import EntryDAL

router = APIRouter(
    prefix="/entries",
    tags=["Entries"]
)


async def get_entry_dal():
    async with async_session() as session:
        async with session.begin():
            yield EntryDAL(session)


@router.post("/", status_code=201,
             responses={500: {"model": mt.Message}},
             description=doc_strings.CREATE_ENTRY)
async def add_entry(entry: EntryCreate, db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.add_entry(entry)
        return mt.Message(
            detail="Entry successfully added!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/", status_code=200,
            responses={500: {"model": mt.Message}})
async def retrieve_entries(sort: str = "lemma", offset: int = None, limit: int = None,
                           db: EntryDAL = Depends(get_entry_dal)):
    filters = {
        "sort": sort,
        "offset": offset,
        "limit": limit
    }
    try:
        return await db.retrieve_entries(filters)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{entry_id}", status_code=200,
            responses={500: {"model": mt.Message}, 404: {"model": mt.Message}, 200: {"model": Entry}})
async def retrieve_entry(entry_id: int, db: EntryDAL = Depends(get_entry_dal)):
    try:
        entry = await db.retrieve_entry_by_id(entry_id)
        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entry not found"
            )
        return entry
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
