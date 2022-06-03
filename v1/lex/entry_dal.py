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
        entries, count = await models.Entry.retrieve_all(filters, self.db_session)
        schema_entries = schemas.Entry.list_from_model(entries)
        schema = schemas.EntryList(
            entries=schema_entries,
            full_count=count
        )
        return schema

    async def retrieve_entry_by_id(self, entry_id: int):
        entry = await models.Entry.retrieve_by_id(entry_id, self.db_session)
        suggestions = await models.Suggestion.retrieve_by_parent(entry_id, self.db_session)
        translation, state = await models.Translation.retrieve_by_parent(entry_id, self.db_session)

        schema = schemas.EntryDetail.from_models(entry, suggestions, translation, state)
        return schema

    async def update_entry(self, entry_update: schemas.EntryUpdate, entry_id: int):
        entry = entry_update.to_model(entry_id)
        await entry.update(self.db_session)

    async def add_suggestion(self, original_term: int, translation: int):
        await models.Suggestion.save(original_term, translation, self.db_session)

    async def remove_suggestion(self, original_term: int, translation: int):
        await models.Suggestion.delete(original_term, translation, self.db_session)

    async def add_translation(self, original_term: int, translation: int, state: int):
        await models.Translation.delete(original_term, self.db_session)
        await models.Translation.save(original_term, translation, state, self.db_session)

    async def manage_translation_state(self, original_term: int, translation: int, state: int):
        await models.Translation.update(original_term, translation, state, self.db_session)

    async def remove_translation(self, original_term: int):
        await models.Translation.delete(original_term, self.db_session)

    async def add_relation(self, entry1: int, entry2: int):
        await models.Relation.save(entry1, entry2, self.db_session)

    async def remove_relation(self, entry1: int, entry2: int):
        await models.Relation.delete(entry1, entry2, self.db_session)
