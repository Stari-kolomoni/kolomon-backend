from typing import Optional, List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import text, insert

from .database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    lemma = Column(String, index=True)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, onupdate=func.now(), nullable=True)

    __mapper__args = {'eager_defaults': True}

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        if (self.lemma != other.lemma
                or self.description != other.description
                or self.id != other.id
                or self.language != other.language):
            return False
        return True

    async def save(self, db_session: Session):
        stmt = insert(Entry).values(
            lemma=self.lemma,
            description=self.description,
            language=self.language
        )
        try:
            result = await db_session.execute(
                stmt
            )

            await db_session.flush()
            self.id = result.inserted_primary_key[0]
            await db_session.commit()

        except Exception as e:
            await db_session.rollback()
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
                await db_session.commit()
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
        await db_session.commit()

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
    async def retrieve_by_entry(entry_id: int, db_session: Session) -> List['Link']:
        pass

    @staticmethod
    async def retrieve_by_id(link_id: int, db_session: Session) -> Optional['Link']:
        pass


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    async def save(self, db_session: Session):
        pass

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_entry(entry_id: int, db_session: Session) -> List['Category']:
        pass

    @staticmethod
    async def retrieve_by_id(category_id: int, db_session: Session) -> Optional['Category']:
        pass


class Slovene(Base):
    __tablename__ = "slovene"

    id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                primary_key=True)
    alt_form = Column(String, nullable=True)

    async def save(self, db_session: Session):
        pass

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_id(entry_id: int, db_session: Session) -> Optional['Slovene']:
        pass


class English(Base):
    __tablename__ = "english"

    id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                primary_key=True)

    async def save(self, db_session: Session):
        pass

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_id(entry_id: int, db_session: Session) -> Optional['English']:
        pass


class Suggestion(Base):
    __tablename__ = "suggestions"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)

    async def save(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_parent(entry_id: int, db_session: Session) -> List['Entry']:
        pass

    @staticmethod
    async def retrieve_by_child(entry_id: int, db_session: Session) -> List['Entry']:
        pass


class Translation(Base):
    __tablename__ = "translations"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)
    state = Column(Integer, ForeignKey('translation_states.id',
                                       ondelete="SET NULL"))

    async def save(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_parent(parent_id: int, db_session: Session) -> Optional['Entry']:
        pass

    @staticmethod
    async def retrieve_by_child(child_id: int, db_session: Session) -> Optional['Entry']:
        pass


class TranslationState(Base):
    __tablename__ = "translation_states"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)

    async def save(self, db_session: Session):
        pass

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_id(state_id: int, db_session: Session) -> Optional['TranslationState']:
        pass


class Relation(Base):
    __tablename__ = "relations"

    entry1 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    entry2 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)

    async def save(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_entry1(entry1: int, db_session: Session) -> List['Entry']:
        pass

    @staticmethod
    async def retrieve_by_entry2(entry1: int, db_session: Session) -> List['Entry']:
        pass


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

    async def save(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve(filters: dict, db_session: Session) -> Optional['Event']:
        pass
