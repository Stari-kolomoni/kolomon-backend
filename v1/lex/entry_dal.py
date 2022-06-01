import traceback
from typing import Optional

from sqlalchemy import text, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import core.models.lex_model as models
import core.schemas.lex_schema as schemas


class EntryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_entry(self, entry_create: schemas.EntryCreate):
        entry = entry_create.to_entry_instance()
        await entry.save(self.db_session)

    async def retrieve_entries(self, filters):
        entries = await models.Entry.retrieve_all(filters, self.db_session)
        return entries

    async def retrieve_entry_by_id(self, entry_id):
        entry = await models.Entry.retrieve_by_id(entry_id, self.db_session)
        return entry
