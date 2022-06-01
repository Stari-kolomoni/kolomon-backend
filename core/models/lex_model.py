from typing import Optional, List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import text, insert, update, delete, desc
from sqlalchemy.future import select

from .database import Base


LIMIT_SIZE = 25


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    lemma = Column(String, index=True)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, onupdate=func.now(), nullable=True)
    extra_data = {}

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

    def __repr__(self):
        return f"Entry[{self.id}]: {self.lemma}"

    async def save(self, db_session: Session):
        stmt = insert(Entry).values(
            lemma=self.lemma,
            description=self.description,
            language=self.language
        )
        result = await db_session.execute(stmt)
        await db_session.flush()
        self.id = result.inserted_primary_key[0]

        if self.language == 'sl':
            alt_form = self.extra_data.get('alternative_form', None)
            await Slovene(
                id=self.id,
                alt_form=alt_form
            ).save(db_session)
        elif self.language == 'en':
            await English(
                id=self.id
            ).save(db_session)

    async def update(self, db_session: Session) -> int:
        stmt = update(Entry).values({
            "lemma": self.lemma,
            "description": self.description,
            "language": self.language
        }).where(Entry.id == self.id)

        result = await db_session.execute(stmt)
        return result.rowcount

    @staticmethod
    async def delete(entry_id: int, db_session: Session):
        stmt = delete(Entry).where(Entry.id == entry_id)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_id(entry_id: int, db_session: Session) -> Optional['Entry']:
        stmt = select(Entry).where(Entry.id == entry_id)
        result = await db_session.execute(stmt)

        entry: Optional[Entry] = result.scalars().first()
        if not entry:
            return None

        if entry.language == 'sl':
            slovene = await Slovene.retrieve_by_id(entry.id, db_session)
            if slovene:
                entry.extra_data = {
                    "alternative_form": slovene.alt_form
                }

        return entry

    @staticmethod
    async def retrieve_all(filters: dict, db_session: Session) -> List['Entry']:
        offset: int = filters.get('offset', 0)
        limit: int = filters.get('limit', LIMIT_SIZE)
        sort: str = filters.get('sort', '')

        stmt = select(Entry)

        sort_list = []
        if "-lemma" in sort:
            sort_list.append(desc("lemma"))
        elif "lemma" in sort:
            sort_list.append("lemma")
        if "-description" in sort:
            sort_list.append(desc("description"))
        elif "description" in sort:
            sort_list.append("description")
        if "-language" in sort:
            sort_list.append(desc("language"))
        elif "language" in sort:
            sort_list.append("language")
        stmt = stmt.order_by(*sort_list)
        stmt = stmt.offset(offset).limit(limit)

        result = await db_session.execute(stmt)

        entries = result.all()
        return entries


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    url = Column(String, index=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))

    async def save(self, db_session: Session):
        stmt = insert(Link).values(
            title=self.title,
            url=self.url,
            entry_id=self.entry_id
        )
        try:
            result = await db_session.execute(stmt)
            await db_session.flush()
            self.id = result.inserted_primary_key[0]
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e

    async def update(self, db_session: Session):
        update_sql = text("UPDATE links "
                          "SET title = :title, url = :url, entry_id = :entry_id "
                          "WHERE id = :id")
        try:
            result = await db_session.execute(
                update_sql,
                {
                    "title": self.title,
                    "url": self.url,
                    "entry_id": self.entry_id
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

    @staticmethod
    async def delete(entry_id: int, db_session: Session):
        delete_sql = text("DELETE FROM links WHERE id = :id")
        await db_session.execute(
            delete_sql,
            {
                "id": entry_id
            }
        )
        await db_session.commit()

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
        stmt = insert(Slovene).values(
            id=self.id,
            alt_form=self.alt_form
        )
        await db_session.execute(stmt)

    async def update(self, db_session: Session):
        pass

    async def delete(self, db_session: Session):
        pass

    @staticmethod
    async def retrieve_by_id(slovene_id: int, db_session: Session) -> Optional['Slovene']:
        stmt = select(Slovene).where(Slovene.id == slovene_id)
        result = await db_session.execute(stmt)

        entry = result.scalars().first()
        if not entry:
            return None
        return entry


class English(Base):
    __tablename__ = "english"

    id = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                primary_key=True)

    async def save(self, db_session: Session):
        stmt = insert(English).values(
            id=self.id
        )
        await db_session.execute(stmt)

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
