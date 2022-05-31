import traceback
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, ArgumentError, DBAPIError
from sqlalchemy.orm import Session

from fastapi import HTTPException

import core.models.lex_model as lm
import core.schemas.lex_schema as ls
from core.exceptions import GeneralBackendException


class LexiconDAL:
    """
    A Data Access Layer for Lexicon application.
    Initialization requires a database session.
    Each of the functions can potentially return a GeneralBackendException.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def entry_exists(self, entry_id: int) -> bool:
        """
        Checks if entry exists.
        Returns True if it does, else False.
        """

        sql = text("EXISTS (SELECT id FROM entries e WHERE e.id = :id)")
        result = await self.db_session.execute(sql, {"id": entry_id})
        return result.scalar()

    async def translation_status_exists(self, status_id: int) -> bool:
        """
        Checks if translation status record exists.
        Returns True if it does, else False.
        """

        sql = text("EXISTS (SELECT id FROM translation_states WHERE id = :id)")
        result = await self.db_session.execute(sql, {"id": status_id})
        return result.scalar()

    async def create_entry(self, entry: lm.Entry) -> bool:
        """
        Creates a new entry record in the database.
        Returns True if successful, else False.
        """

        try:
            self.db_session.add(entry)
            await self.db_session.flush()
            return True
        except Exception:
            await self.db_session.rollback()
            return False

    async def delete_entry(self, entry_id: int) -> bool:
        """
        Deletes entry record from the database.
        Returns true if successful, else False.
        """

        sql = text("DELETE FROM entries WHERE id = :id")
        result_cursor = await self.db_session.execute(sql, {"id": entry_id})
        affected_rows_count = result_cursor.rowcount
        if affected_rows_count > 0:
            await self.db_session.flush()
            return True
        else:
            await self.db_session.rollback()
            return False

    async def update_entry(self, entry_id: int, updates: lm.Entry) -> bool:
        """
        Updates entry data in the database.
        Returns True if successful, else False.
        """

        sql = text("UPDATE entries "
                   "SET lemma = :lemma, description = :description, modified = NOW() "
                   "WHERE id = :id")
        result_cursor = await self.db_session.execute(sql, {"id": entry_id,
                                                            "lemma": updates.lemma,
                                                            "description": updates.description})
        affected_rows_count = result_cursor.rowcount
        if affected_rows_count > 0:
            await self.db_session.flush()
            return True
        else:
            await self.db_session.rollback()
            return False

    async def get_entry_by_id(self, entry_id: int) -> Optional[ls.Entry]:
        """
        Retrieves all entry information by its id field.
        If information could not be retrieved, returns None.
        """

        entry_sql = text("SELECT * FROM entries e WHERE e.id = :id")
        entry_result_cursor = await self.db_session.execute(entry_sql,
                                                            {"id": entry_id})
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

    async def get_entry_pair(self, entry_id: int) -> ls.EntryPair:
        """
        Retrieves entry pair - English entry and/or its Slovene counterpart.
        Either can also be None.
        """

        original = await self.get_entry_by_id(entry_id)

        translation_sql = text("SELECT * FROM translations "
                               "INNER JOIN translation_states ON translations.state = translation_states.id "
                               "WHERE translations.parent = :id")

        translation_result_cursor = await self.db_session.execute(translation_sql,
                                                                  {"id": entry_id})
        translation_result = translation_result_cursor.first()

        translation = None
        translation_state = None
        if translation_result:
            child_id = translation_result[1]
            if child_id:
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

    async def create_link(self, link: lm.Link) -> bool:
        """
        Creates a new link record in the database.
        """

        try:
            self.db_session.add(link)
            await self.db_session.flush()
            return True
        except Exception:
            await self.db_session.rollback()
            return False

    async def create_suggestion(self, parent_id: int, child_id: int):
        """
        Creates suggestion in the database.
        Requires only both entries' id's for linkage.
        """

        sql = text("INSERT INTO suggestions VALUES (:parent, :child)")
        try:
            await self.db_session.execute(sql,
                                          {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while inserting new suggestion."
            )

    async def delete_suggestion(self, parent_id: int, child_id: int):
        """
        Deletes suggestion linkage from the database.
        Requires only both entries' id's for linkage.
        Can potentially raise HTTPException.
        """

        sql = text("DELETE FROM suggestions WHERE parent = :parent AND child = :child")
        try:
            await self.db_session.execute(sql,
                                          {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while deleting suggestion."
            )

    async def retrieve_suggestions(self, entry_id: int) -> List[ls.EntryMinimal]:
        """
        Retrieves suggestions from the database.
        """

        suggestions: List[ls.EntryMinimal] = []
        sql = text("SELECT entries.id, entries.lemma, entries.description, entries.language "
                   "FROM suggestions INNER JOIN entries ON suggestions.child = entries.id "
                   "WHERE suggestions.parent = :id")
        suggestions_result = await self.db_session.execute(sql,
                                                           {"id": entry_id})
        for suggestion in suggestions_result.all():
            suggestion_entry = ls.EntryMinimal.from_sql(suggestion)
            suggestions.append(suggestion_entry)

        return suggestions

    async def create_translation(self, parent_id: int, child_id: int, status: Optional[int]):
        """
        Creates translation in the database.
        Requires both entries' id's for linkage. Status is optional.
        Can potentially raise HTTPException.
        """

        await self.delete_translations_of_parent(parent_id)

        insert_sql = text("INSERT INTO translations VALUES (:parent, :child, :status)")
        try:
            await self.db_session.execute(insert_sql,
                                          {"parent": parent_id, "child": child_id, "status": status})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while inserting new translation."
            )

    async def delete_translations_of_parent(self, parent_id: int):
        """
        Deletes all translations of the entry.
        Can potentially raise HTTPException.
        """

        sql = text("DELETE FROM translations WHERE parent = :parent")
        try:
            await self.db_session.execute(sql,
                                          {"parent": parent_id})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while deleting translations."
            )

    async def get_translation_state_by_label(self, label: str) -> Optional[ls.TranslationState]:
        """
        Retrieves translation state record based on its label.
        Since label in the database as of this writing is not
        enforced unique, we cannot be sure there are not many
        states with the same label. Method therefore selects
        the first entry it acquires.
        """

        sql = text("SELECT * FROM translation_states WHERE label = :label")
        state_result_cursor = await self.db_session.execute(sql,
                                                            {"label": label})
        state_result = state_result_cursor.first()
        if not state_result:
            return None

        state = ls.TranslationState(
            id=state_result[0],
            label=state_result[1]
        )
        return state

    async def create_relation(self, parent_id: int, child_id: int):
        """
        Creates new relation in the database.
        Requires both entries' id's for linkage.
        Can potentially raise HTTPException.
        """

        sql = text("INSERT INTO relations VALUES (:parent, :child)")
        try:
            await self.db_session.execute(sql,
                                          {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while inserting new relation."
            )

    async def delete_relation(self, parent_id: int, child_id: int):
        """
        Deletes given relation from the database.
        Requires both entries' id's for linkage.
        Can potentially raise HTTPException.
        """

        sql = text("DELETE FROM relations WHERE entry1 = :parent AND entry2 = :child")
        try:
            await self.db_session.execute(sql,
                                          {"parent": parent_id, "child": child_id})
            await self.db_session.flush()
        except:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=500,
                detail="An error occurred while deleting relation."
            )
