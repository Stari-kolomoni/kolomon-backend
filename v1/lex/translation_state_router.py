from fastapi import APIRouter, Depends, HTTPException

import core.schemas.message_types as mt
from core.models.database import async_session
from core.schemas.lex_schema import *
from v1.lex.translation_state_dal import TranslationStateDAL

router = APIRouter(
    prefix="/translation_state",
    tags=["Translation state"]
)


async def get_state_dal():
    async with async_session() as session:
        async with session.begin():
            yield TranslationStateDAL(session)


@router.post("/", status_code=201,
             responses={500: {"model": mt.Message}})
async def add_translation_state(state: TranslationStateCreate,
                                db: TranslationStateDAL = Depends(get_state_dal)):
    try:
        await db.add_translation_state(state)
        return mt.Message(
            detail="Translation state successfully added!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/", status_code=200,
            responses={500: {"model": mt.Message}})
async def retrieve_translation_states(offset: int = None, limit: int = None,
                                      db: TranslationStateDAL = Depends(get_state_dal)):
    filters = {
        "offset": offset,
        "limit": limit
    }
    try:
        schema = await db.retrieve_all_translation_states(filters)
        return schema
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.get("/{state_id}", status_code=200,
            responses={500: {"model": mt.Message},
                       404: {"model": mt.Message},
                       200: {"model": TranslationState}})
async def retrieve_translation_state(state_id: int,
                                     db: TranslationStateDAL = Depends(get_state_dal)):
    try:
        state = await db.retrieve_translation_state_by_id(state_id)
        if not state:
            raise HTTPException(
                status_code=404,
                detail="Translation state not found"
            )
        return state
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )


@router.delete("/{state_id}", status_code=200,
               responses={500: {"model": mt.Message},
                          200: {"model": mt.Message}})
async def remove_translation_state(state_id: int,
                                   db: TranslationStateDAL = Depends(get_state_dal)):
    try:
        await db.remove_translation_state(state_id)
        return mt.Message(
            detail="Translation state deleted!"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
