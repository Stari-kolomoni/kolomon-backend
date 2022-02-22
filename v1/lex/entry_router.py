from typing import Union

from fastapi import APIRouter, Depends

import core.message_types as mt
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


@router.post("/", status_code=201, response_model=mt.Message,
             responses={400: {"model": mt.Message},
                        500: {"model": mt.Message}},
             description=doc_strings.CREATE_ENTRY)
async def add_entry(entry: EntryCreate, db: EntryDAL = Depends(get_entry_dal)):
    status = await db.create_entry(entry)
    if status == 200:
        return mt.Message(detail="Entry successfully added")
    if status == 400:
        raise GeneralBackendException(400, "Invalid entry")
    raise GeneralBackendException(500, "Error adding entry")


@router.get("/{entry_id}", status_code=200, response_model=EntryPair,
            responses={404: {"model": mt.Message}},
            description=doc_strings.GET_ENTRY_PAIR)
async def read_entry_pair(entry_id: int, db: EntryDAL = Depends(get_entry_dal)):
    entry_pair = await db.get_entry_pair(entry_id)
    if not entry_pair:
        raise GeneralBackendException(404, "Entry not found")
    return entry_pair


@router.put("/{entry_id}", status_code=200, response_model=mt.Message,
            responses={404: {"model": mt.Message},
                       500: {"model": mt.Message}},
            description=doc_strings.UPDATE_ENTRY)
async def update_entry(entry_id: int, updates: EntryUpdate,
                       db: EntryDAL = Depends(get_entry_dal)):
    status = await db.update_entry(entry_id, updates)
    if status == 200:
        return mt.Message(detail="Entry successfully updated")
    elif status == 404:
        raise GeneralBackendException(404, "Entry not found")
    raise GeneralBackendException(500, "Error updating entry")


@router.delete("/{entry_id}", status_code=200, response_model=mt.Message,
               responses={404: {"model": mt.Message},
                          500: {"model": mt.Message}},
               description=doc_strings.DELETE_ENTRY)
async def remove_entry(entry_id: int, db: EntryDAL = Depends(get_entry_dal)):
    status = await db.delete_entry(entry_id)
    if status == 200:
        return mt.Message(detail="Entry successfully deleted")
    elif status == 404:
        raise GeneralBackendException(404, "Entry not found")
    raise GeneralBackendException(500, "Error removing entry")


@router.post("/{entry_id}/link", status_code=201, response_model=mt.Message,
             responses={400: {"model": mt.Message},
                        404: {"model": mt.Message},
                        500: {"model": mt.Message}},
             description=doc_strings.LINK_CREATE)
async def add_link(entry_id: int, link: LinkCreate,
                   db: EntryDAL = Depends(get_entry_dal)):
    status = await db.create_link(link, entry_id)
    if status == 200:
        return mt.Message(detail=f"Link successfully added to entry with ID {entry_id}.")
    elif status == 400:
        raise GeneralBackendException(400, "Invalid link")
    elif status == 404:
        raise GeneralBackendException(404, "Entry not found")
    raise GeneralBackendException(500, "Error adding link")


@router.get("/{entry_id}/suggest", status_code=201, response_model=mt.Message,
            responses={404: {"model": mt.Message},
                       500: {"model": mt.Message}},
            description=doc_strings.CREATE_SUGGESTION)
async def add_suggestion(entry_id: int, child_id: int,
                         db: EntryDAL = Depends(get_entry_dal)):
    status = await db.create_suggestion(entry_id, child_id)
    if status == 200:
        return mt.Message(detail=f"Suggestion with ID {child_id} added to entry with ID {entry_id}.")
    elif status == 404:
        raise GeneralBackendException(404, "Entry not found")
    raise GeneralBackendException(500, "Error adding suggestion")


@router.delete("/{entry_id}/suggest", status_code=200, response_model=mt.Message,
               responses={500: {"model": mt.Message}},
               description=doc_strings.DELETE_SUGGESTION)
async def remove_suggestion(entry_id: int, child_id: int,
                            db: EntryDAL = Depends(get_entry_dal)):
    status = await db.delete_suggestion(entry_id, child_id)
    if status == 200:
        return mt.Message(detail=f"Suggestion with ID {child_id} removed from entry with ID {entry_id}.")
    raise GeneralBackendException(500, "Error removing suggestion")


@router.get("/{entry_id}/translate", status_code=201, response_model=mt.Message,
            responses={404: {"model": mt.Message},
                       500: {"model": mt.Message}},
            description=doc_strings.CREATE_TRANSLATION)
async def add_translation(entry_id: int, translation_id: int, status: Union[int, str],
                          db: EntryDAL = Depends(get_entry_dal)):
    status_id = status
    if type(status) is str:
        state_obj = await db.get_translation_state_by_label(status)
        if not state_obj:
            raise GeneralBackendException(404, "Entry or translation state not found")
        status_id = state_obj.id

    insertion_status = await db.create_translation(entry_id, translation_id, status_id)
    if insertion_status == 200:
        return mt.Message(detail=f"Translation with ID {translation_id} added to entry with ID {entry_id}.")
    elif insertion_status == 404:
        raise GeneralBackendException(404, "Entry or translation state not found")
    raise GeneralBackendException(500, "Error adding suggestion")


@router.delete("/{entry_id}/translate", status_code=200, response_model=mt.Message,
               responses={500: {"model": mt.Message}},
               description=doc_strings.DELETE_TRANSLATION)
async def remove_translation(entry_id: int, db: EntryDAL = Depends(get_entry_dal)):
    status = await db.delete_translations_of_parent(entry_id)
    if status == 200:
        return mt.Message(detail=f"Translation removed from entry with ID {entry_id}.")
    raise GeneralBackendException(500, "Error removing translation")


@router.get("/{entry_id}/relate", status_code=201, response_model=mt.Message,
            responses={404: {"model": mt.Message},
                       500: {"model": mt.Message}},
            description=doc_strings.CREATE_RELATION)
async def add_entry_relation(entry_id: int, related_id: int,
                             db: EntryDAL = Depends(get_entry_dal)):
    status = await db.create_relation(entry_id, related_id)
    if status == 200:
        return mt.Message(detail=f"Made relation from ID {entry_id} to ID {related_id}.")
    elif status == 404:
        raise GeneralBackendException(404, "Entry not found")
    raise GeneralBackendException(500, "Error adding relation")


@router.delete("/{entry_id}/relate", status_code=200, response_model=mt.Message,
               responses={500: {"model": mt.Message}},
               description=doc_strings.DELETE_RELATION)
async def remove_entry_relation(entry_id: int, related_id: int,
                                db: EntryDAL = Depends(get_entry_dal)):
    status = await db.delete_relation(entry_id, related_id)
    if status == 200:
        return mt.Message(detail=f"Relation from ID {entry_id} to ID {related_id} removed.")
    raise GeneralBackendException(500, "Error removing relation")
