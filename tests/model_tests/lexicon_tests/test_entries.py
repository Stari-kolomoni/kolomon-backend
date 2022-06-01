from core.models.database import async_session
from core.models.lex_model import Entry
import pytest
from tests.database_handler import db


class TestEntryBatch:
    pass
    '''@pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_update_delete_normal(self, db):
        """
        Tests updating and deleting records.
        """

        number_of_entries = 5
        entry_ids = []

        for i in range(number_of_entries):
            insert_entry = Entry(
                lemma='Default lemma',
                description='Default description',
                language='en'
            )
            await insert_entry.save(db)
            entry_ids.append(insert_entry.id)

        # Updating lemma
        entry = await Entry.retrieve(entry_ids[0], db)
        entry.lemma = "Different lemma"
        await entry.update(db)
        retrieve_entry = await Entry.retrieve(entry_ids[0], db)
        assert (retrieve_entry == entry)

        # Updating description
        entry = await Entry.retrieve(entry_ids[1], db)
        entry.description = "Different description"
        await entry.update(db)
        retrieve_entry = await Entry.retrieve(entry_ids[1], db)
        assert (retrieve_entry == entry)

        # Updating language
        entry = await Entry.retrieve(entry_ids[2], db)
        entry.language = 'sl'
        await entry.update(db)
        retrieve_entry = await Entry.retrieve(entry_ids[2], db)
        assert (retrieve_entry == entry)

        # Updating all
        entry = await Entry.retrieve(entry_ids[3], db)
        entry.lemma = "Different lemma"
        entry.description = "Different description"
        entry.language = 'sl'
        await entry.update(db)
        retrieve_entry = await Entry.retrieve(entry_ids[3], db)
        assert (retrieve_entry == entry)

        for i in range(number_of_entries):
            await Entry.delete(entry_ids[i], db)
            await Entry.retrieve(entry_ids[i], db)'''
