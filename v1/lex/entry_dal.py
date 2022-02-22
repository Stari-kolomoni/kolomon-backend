import traceback
from typing import Optional

from sqlalchemy import text, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import core.models.lex_model as lm
import core.schemas.lex_schema as ls


class EntryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def entry_exists(self, entry_id: int) -> bool:
        sql = text("SELECT id FROM entries e WHERE e.id = :id")
        result = await self.db_session.execute(sql, {"id": entry_id})
        if result.first():
            return True
        return False

    async def translation_status_exists(self, status_id: int) -> bool:
        sql = text("SELECT id FROM translation_states WHERE id = :id")
        result = await self.db_session.execute(sql, {"id": status_id})
        if result.first():
            return True
        return False

    async def create_entry(self, entry: ls.EntryCreate) -> int:
        db_entry = lm.Entry.from_schema(entry)
        if not db_entry:
            return 400
        self.db_session.add(db_entry)

        try:
            await self.db_session.flush()
            await self.db_session.refresh(db_entry)

            if entry.language:
                if entry.language == 'sl':
                    self.db_session.add(lm.Slovene(
                        id=db_entry.id,
                        alt_form=None
                    ))
                elif entry.language == 'en':
                    self.db_session.add(lm.English(
                        id=db_entry.id
                    ))
                await self.db_session.flush()
            return 200
        except:
            await self.db_session.rollback()
            return 500

    async def delete_entry(self, entry_id: int) -> int:
        sql = text("DELETE FROM entries WHERE id = :id")
        try:
            result_cursor = await self.db_session.execute(sql, {"id": entry_id})
            affected_rows_count = result_cursor.rowcount
            if affected_rows_count > 0:
                await self.db_session.flush()
                return 200
            else:
                await self.db_session.rollback()
                return 404
        except:
            await self.db_session.rollback()
            return 500

    async def update_entry(self, entry_id: int, updates: ls.EntryUpdate):
        sql = text("UPDATE entries "
                   "SET lemma = :lemma, description = :description, modified = NOW() "
                   "WHERE id = :id")
        try:
            result_cursor = await self.db_session.execute(sql, {"id": entry_id,
                                                                "lemma": updates.lemma,
                                                                "description": updates.description})
            affected_rows_count = result_cursor.rowcount
            if affected_rows_count > 0:
                await self.db_session.flush()
                return 200
            else:
                await self.db_session.rollback()
                return 404
        except:
            print(traceback.format_exc())
            await self.db_session.rollback()
            return 500

    async def create_link(self, link: ls.LinkCreate, entry_id: int) -> int:
        if not await self.entry_exists(entry_id):
            return 404

        db_link = lm.Link.from_schema_from_id(link, entry_id)
        if not db_link:
            return 400

        self.db_session.add(db_link)

        try:
            await self.db_session.flush()
            return 200
        except:
            await self.db_session.rollback()
            return 500

    async def get_entry_by_id(self, entry_id: int) -> Optional[ls.Entry]:
        entry_sql = text("SELECT * FROM entries e WHERE e.id = :id")
        entry_result_cursor = await self.db_session.execute(entry_sql, {"id": entry_id})
        entry_result = entry_result_cursor.first()
        if not entry_result:
            return None
        entry = ls.Entry.from_sql(entry_result)

        suggestions_sql = text("SELECT entries.id, entries.lemma, entries.description, entries.language "
                               "FROM suggestions INNER JOIN entries ON suggestions.child = entries.id "
                               "WHERE suggestions.parent = :id")
        suggestions_result = await self.db_session.execute(suggestions_sql,
                                                           {"id": entry.id})
        for suggestion in suggestions_result.all():
            suggestion_entry = ls.EntryMinimal.from_sql(suggestion)
            entry.suggestions.append(suggestion_entry)

        relations_sql = text("SELECT entries.id, entries.lemma, entries.description, entries.language "
                             "FROM relations INNER JOIN entries ON relations.entry2 = entries.id "
                             "WHERE relations.entry1 = :id")
        relations_result = await self.db_session.execute(relations_sql,
                                                                  {"id": entry.id})
        for relation in relations_result.all():
            relation_entry = ls.EntryMinimal.from_sql(relation)
            entry.relations.append(relation_entry)

        links_sql = text("SELECT * FROM links WHERE links.entry_id = :id")
        links_result = await self.db_session.execute(links_sql,
                                                     {"id": entry.id})
        for link in links_result.all():
            link_obj = ls.Link.from_sql(link)
            entry.links.append(link_obj)

        return entry

    async def get_entry_pair(self, entry_id: int) -> Optional[ls.EntryPair]:
        original = await self.get_entry_by_id(entry_id)
        if not original:
            return None

        translation_sql = text("SELECT * FROM translations "
                               "INNER JOIN translation_states ON translations.state = translation_states.id "
                               "WHERE translations.parent = :id")
        translation_result_cursor = await self.db_session.execute(translation_sql, {"id": entry_id})
        translation_result = translation_result_cursor.first()

        translation = None
        translation_state = None
        if translation_result:
            child_id = translation_result[1]

            translation = await self.get_entry_by_id(child_id)

            translation_state = ls.TranslationState(
                id=translation_result[3],
                label=translation_result[4]
            )

        entry_pair = ls.EntryPair(
            original=original,
            translation=translation,
            translation_state=translation_state
        )

        return entry_pair

    async def create_suggestion(self, parent_id: int, child_id: int) -> int:
        if (not await self.entry_exists(parent_id)
                or not await self.entry_exists(child_id)):
            return 404

        sql = text("INSERT INTO suggestions VALUES (:parent, :child)")
        try:
            await self.db_session.execute(sql, {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
            return 200
        except IntegrityError:
            await self.db_session.rollback()
        return 500

    async def delete_suggestion(self, parent_id: int, child_id: int) -> int:
        sql = text("DELETE FROM suggestions WHERE parent = :parent AND child = :child")
        try:
            await self.db_session.execute(sql, {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
            return 200
        except:
            await self.db_session.rollback()
        return 500

    async def delete_translations_of_parent(self, parent_id: int) -> int:
        sql = text("DELETE FROM translations WHERE parent = :parent")
        try:
            await self.db_session.execute(sql, {"parent": parent_id})
            await self.db_session.flush()
            return 200
        except:
            await self.db_session.rollback()
        return 500

    async def create_translation(self, parent_id: int, child_id: int, status: int) -> int:
        if (not await self.entry_exists(parent_id)
                or not await self.entry_exists(child_id)
                or not await self.translation_status_exists(status)):
            return 404

        delete_sql = text("DELETE FROM translations WHERE parent = :parent")
        insert_sql = text("INSERT INTO translations VALUES (:parent, :child, :status)")
        try:
            await self.db_session.execute(delete_sql, {"parent": parent_id})
            await self.db_session.execute(insert_sql, {"parent": parent_id,
                                                       "child": child_id,
                                                       "status": status})
            await self.db_session.flush()
            return 200
        except IntegrityError:
            await self.db_session.rollback()
        return 500

    async def get_translation_state_by_label(self, label: str) -> Optional[ls.TranslationState]:
        sql = text("SELECT * FROM translation_states WHERE label = :label")
        state_result_cursor = await self.db_session.execute(sql, {"label": label})
        state_result = state_result_cursor.first()
        if not state_result:
            return None

        state = ls.TranslationState(
            id=state_result[0],
            label=state_result[1]
        )
        return state

    async def create_relation(self, parent_id: int, child_id: int) -> int:
        if (not await self.entry_exists(parent_id)
                or not await self.entry_exists(child_id)):
            return 404

        sql = text("INSERT INTO relations VALUES (:parent, :child)")
        try:
            await self.db_session.execute(sql, {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
            return 200
        except IntegrityError:
            await self.db_session.rollback()
        return 500

    async def delete_relation(self, parent_id: int, child_id: int) -> int:
        sql = text("DELETE FROM relations WHERE entry1 = :parent AND entry2 = :child")
        try:
            await self.db_session.execute(sql, {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
            return 200
        except:
            await self.db_session.rollback()
        return 500
