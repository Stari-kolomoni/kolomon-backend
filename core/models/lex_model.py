from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import Base
from ..schemas import lex_schema as ls


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    lemma = Column(String, index=True)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, onupdate=func.now(), nullable=True)

    __mapper__args = {'eager_defaults': True}

    async def save(self, db_session: Session):
        insert_sql = text("INSERT INTO entries (lemma, description, language) "
                          "VALUES (:lemma, :description, :language)")
        try:
            result = await db_session.execute(
                insert_sql,
                {
                    "lemma": self.lemma,
                    "description": self.description,
                    "language": self.language
                }
            )

            await db_session.commit()
            self.id = result.inserted_primary_key[0]
            db_session.flush()

        except Exception as e:
            db_session.rollback()
            raise e

    async def update(self, db_session: Session):
        update_sql = text("UPDATE entries "
                          "SET lemma = :lemma, description = :description, modified = NOW() "
                          "WHERE id = :id")
        try:
            result = await db_session.execute(
                update_sql,
                {
                    "lemma": self.lemma,
                    "description": self.description,
                    "id": self.id
                }
            )

            affected_rows_count = result.rowcount
            if affected_rows_count > 0:
                await db_session.flush()
            else:
                await db_session.rollback()

        except Exception as e:
            await db_session.rollback()
            raise e

    async def delete(self, db_session: Session):
        delete_sql = text("DELETE FROM entries WHERE id = :id")
        await db_session.execute(
            delete_sql,
            {
                "id": self.id
            }
        )
        await db_session.flush()

    @staticmethod
    async def retrieve(entry_id: int, db_session: Session) -> Optional['Entry']:
        get_sql = text("SELECT * FROM entries e WHERE e.id = :id")
        result = await db_session.execute(
            get_sql,
            {
                "id": entry_id
            }
        )

        row = result.first()
        if not row:
            return None

        entry = Entry(
            id=row[0],
            lemma=row[1],
            description=row[2],
            language=row[3],
            created=row[4],
            modified=row[5]
        )
        return entry


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    url = Column(String, index=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))

    async def save(self, db_session: Session):
        pass

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve(entry_id: int, db_session: Session) -> Optional['Entry']:
        pass


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)


class Slovene(Base):
    __tablename__ = "slovene"

    id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                primary_key=True)
    alt_form = Column(String, nullable=True)


class English(Base):
    __tablename__ = "english"

    id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                primary_key=True)


class Suggestion(Base):
    __tablename__ = "suggestions"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)


class Translation(Base):
    __tablename__ = "translations"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)
    state = Column(Integer, ForeignKey('translation_states.id',
                                       ondelete="SET NULL"))


class TranslationState(Base):
    __tablename__ = "translation_states"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)


class Relation(Base):
    __tablename__ = "relations"

    entry1 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    entry2 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)


class CategoryToEntry(Base):
    __tablename__ = "category_to_entry"

    entry_id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                      primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"),
                         primary_key=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    table = Column(String)
    action = Column(String)
    record_id = Column(Integer)
    user_id = Column(Integer)
    username = Column(String)
    time = Column(DateTime, server_default=func.now())
