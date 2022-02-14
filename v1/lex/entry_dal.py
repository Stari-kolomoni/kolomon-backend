from sqlalchemy.orm import Session

import core.models.lex_model as lm
import core.schemas.lex_schema as ls


class EntryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_entry(self, entry: ls.EntryCreate) -> int:
        db_entry = lm.Entry.from_schema(entry)
        if not db_entry:
            return 1
        self.db_session.add(db_entry)

        try:
            await self.db_session.flush()
            await self.db_session.refresh(db_entry)
            return 0
        except:
            await self.db_session.rollback()
            return -1
