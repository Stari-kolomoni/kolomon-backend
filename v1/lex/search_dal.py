from typing import Optional

from sqlalchemy.orm import Session

import core.models.lex_model as models
import core.schemas.lex_schema as schemas


class SearchDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def entry_simple_search(self, query: str, filters: dict, language: Optional[str]):
        if language == 'sl':
            entries, count = await models.Entry.simple_search_lang(query, language, filters, self.db_session)
        elif language == 'en':
            entries, count = await models.Entry.simple_search_lang(query, language, filters, self.db_session)
        else:
            entries, count = await models.Entry.simple_search_all(query, filters, self.db_session)
        schema = schemas.EntryMinimal.list_from_model(entries)
        list_schema = schemas.MinimalEntryList(
            entries=schema,
            full_count=count
        )
        return list_schema

    async def entry_full_search(self, query: str, filters: dict, language: Optional[str]):
        if language == 'sl':
            entries, count = await models.Entry.full_search_lang(query, language, filters, self.db_session)
        elif language == 'en':
            entries, count = await models.Entry.full_search_lang(query, language, filters, self.db_session)
        else:
            entries, count = await models.Entry.full_search_lang(query, '', filters, self.db_session)
        schema = schemas.EntryPair.from_list_models(entries)
        list_schema = schemas.EntryPairList(
            entries=schema,
            full_count=count
        )
        return list_schema
