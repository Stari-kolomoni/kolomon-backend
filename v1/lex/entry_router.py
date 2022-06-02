from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

import core.schemas.message_types as mt
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
            responses={500: {"model": mt.Message},
                       200: {"model": EntryList}})
async def retrieve_entries(sort: str = "lemma", offset: int = None, limit: int = None,
                           db: EntryDAL = Depends(get_entry_dal)):
    filters = {
        "sort": sort,
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.retrieve_entries(filters)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{entry_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       404: {"model": mt.Message},
                       200: {"model": EntryDetail}})
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


@router.get("/{entry_id}/suggest/{suggestion_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       200: {"model": mt.Message},
                       404: {"model": mt.Message}})
async def suggest_translation(entry_id: int, suggestion_id: int,
                              db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.add_suggestion(entry_id, suggestion_id)
        return mt.Message(
            detail="Suggestion successfully added!"
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.delete("/{entry_id}/suggest/{suggestion_id}", status_code=200,
               responses={500: {"model": mt.Message},
                          200: {"model": mt.Message}})
async def remove_suggestion(entry_id: int, suggestion_id: int,
                            db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.remove_suggestion(entry_id, suggestion_id)
        return mt.Message(
            detail="Suggestion deleted!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{entry_id}/translate/{translation_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       200: {"model": mt.Message},
                       404: {"model": mt.Message}})
async def add_translation(entry_id: int, translation_id: int,
                          translation_state_id: int = None,
                          db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.add_translation(entry_id, translation_id, translation_state_id)
        return mt.Message(
            detail="Translation successfully added!"
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Entry or state not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.delete("/{entry_id}/translate", status_code=200,
               responses={500: {"model": mt.Message},
                          200: {"model": mt.Message}})
async def remove_translation(entry_id: int, db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.remove_translation(entry_id)
        return mt.Message(
            detail="Translation removed!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{entry_id}/relate/{other_entry_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       200: {"model": mt.Message},
                       404: {"model": mt.Message}})
async def add_relation(entry_id: int, other_entry_id: int,
                       db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.add_relation(entry_id, other_entry_id)
        return mt.Message(
            detail="Relation successfully added!"
        )
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.delete("/{entry_id}/relate/{other_entry_id}", status_code=200,
               responses={500: {"model": mt.Message},
                          200: {"model": mt.Message}})
async def remove_relation(entry_id: int, other_entry_id: int,
                          db: EntryDAL = Depends(get_entry_dal)):
    try:
        await db.remove_relation(entry_id, other_entry_id)
        return mt.Message(
            detail="Relation removed!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
