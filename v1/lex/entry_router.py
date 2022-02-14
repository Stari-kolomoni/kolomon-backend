from fastapi import APIRouter, Depends

import core.message_types as mt
from core.exceptions import GeneralBackendException
from core.models.database import async_session
from core.schemas.lex_schema import *
from v1.lex.entry_dal import EntryDAL

router = APIRouter(
    prefix="/entries",
    tags=["Entries"]
)


async def get_entry_dal():
    async with async_session() as session:
        async with session.begin():
            yield EntryDAL(session)


@router.post("/", status_code=201)
async def add_entry(entry: EntryCreate, db: EntryDAL = Depends(get_entry_dal)):
    success = await db.create_entry(entry)
    if success > 0:
        raise GeneralBackendException(400, "Invalid entry")
    elif success < 0:
        raise GeneralBackendException(500, "Error adding entry.")
    return mt.Message(detail="Entry successfully added.")


@router.get("/{entry_id}", status_code=200)
async def read_entry_pair(entry_id: int):
    pass


@router.post("/{entry_id}/link", status_code=201)
async def create_link(entry_id: int):
    pass


@router.post("/{entry_id}/suggest", status_code=201)
async def create_suggestion(entry_id: int):
    pass


@router.get("/{entry_id}/translate", status_code=201)
async def link_translation(entry_id: int, translation_id: int):
    pass


@router.get("/{entry_id}/relate", status_code=201)
async def create_entry_relation(entry_id: int, related_id: int):
    pass
