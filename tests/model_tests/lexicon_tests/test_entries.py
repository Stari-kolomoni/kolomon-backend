from core.models.database import async_session
from core.models.lex_model import Entry
import pytest
from tests.database_handler import db


class TestEntryBatch:

    @pytest.mark.asyncio
    async def test_insert_retrieve_normal(self, db):
        """
        Tests a basic insert and retrieve with all data provided.
        Tests for insert in English and Slovene language.
        """

        insert_entry_en = Entry(
            lemma='Entry 1',
            description='Description 1',
            language='en'
        )
        insert_entry_sl = Entry(
            lemma='Entry 2',
            description='Description 2',
            language='sl'
        )

        await insert_entry_en.save(db)
        await insert_entry_sl.save(db)

        retrieve_entry_en = await Entry.retrieve(insert_entry_en.id, db)
        retrieve_entry_sl = await Entry.retrieve(insert_entry_sl.id, db)

        assert (insert_entry_en == retrieve_entry_en)
        assert (insert_entry_sl == retrieve_entry_sl)
