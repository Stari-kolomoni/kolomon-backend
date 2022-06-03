from typing import Optional, List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, text
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, desc, and_
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
        """
        Saves to the database the Entry on which the method is executed.
        After successful execution, the 'id' property of this Entry
        is populated with the value assigned to the record in the database.
        NOTE: properties 'created' and 'modified' are not populated,
        a separate retrieval is needed for that.
        """

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
            "description": self.description
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
    async def retrieve_all(filters: dict, db_session: Session) -> (List['Entry'], int):
        offset: int = filters.get('offset', 0)
        limit: int = filters.get('limit', LIMIT_SIZE)
        sort: str = filters.get('sort', '')

        count_stmt = select(func.count(Entry.id))
        count_result = await db_session.execute(count_stmt)
        count = count_result.scalar()

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

        entries = result.scalars().all()
        return entries, count


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
        result = await db_session.execute(stmt)
        await db_session.flush()
        self.id = result.inserted_primary_key[0]

    async def update(self, db_session: Session) -> int:
        pass

    @staticmethod
    async def delete(link_id: int, db_session: Session):
        stmt = delete(Link).where(Link.id == link_id)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_entry(entry_id: int, db_session: Session) -> List['Link']:
        stmt = select(Link).where(Link.entry_id == entry_id)
        result = await db_session.execute(stmt)

        links: List[Link] = result.scalars().all()
        return links

    @staticmethod
    async def retrieve_by_id(link_id: int, db_session: Session) -> Optional['Link']:
        stmt = select(Link).where(Link.id == link_id)
        result = await db_session.execute(stmt)

        link: Optional[Link] = result.scalars().all()
        if not link:
            return None
        return link


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"Category[{self.id}]: {self.name}"

    async def save(self, db_session: Session):
        """
        Saves to the database the Category on which the method is executed.
        After successful execution, the 'id' property of this Category
        is populated with the value assigned to the record in the database.
        """

        stmt = insert(Category).values(
            name=self.name,
            description=self.description
        )
        result = await db_session.execute(stmt)
        await db_session.flush()
        self.id = result.inserted_primary_key[0]

    async def update(self, db_session: Session):
        stmt = update(Category).values({
            "name": self.name,
            "description": self.description
        }).where(Category.id == self.id)
        result = await db_session.execute(stmt)
        return result.rowcount

    @staticmethod
    async def delete(category_id: int, db_session: Session):
        stmt = delete(Category).where(Category.id == category_id)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_entry(entry_id: int, db_session: Session) -> List['Category']:
        stmt = select(Category).filter(CategoryToEntry.entry_id == entry_id,
                                       CategoryToEntry.category_id == Category.id)
        result = await db_session.execute(stmt)

        categories: List[Category] = result.scalars().all()
        return categories

    @staticmethod
    async def retrieve_by_id(category_id: int, db_session: Session) -> Optional['Category']:
        stmt = select(Category).where(Category.id == category_id)
        result = await db_session.execute(stmt)

        category: Optional[Category] = result.scalars().first()
        if not category:
            return None
        return category


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

    async def update(self, db_session: Session) -> int:
        stmt = update(Slovene).values({
            "alt_form": self.alt_form
        }).where(Slovene.id == self.id)

        result = await db_session.execute(stmt)
        return result.rowcount

    @staticmethod
    async def delete(slovene_id: int, db_session: Session):
        stmt = delete(Slovene).where(Slovene.id == slovene_id)
        await db_session.execute(stmt)

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

    @staticmethod
    async def delete(english_id: int, db_session: Session):
        stmt = delete(English).where(English.id == english_id)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_id(english_id: int, db_session: Session) -> Optional['English']:
        stmt = select(English).where(English.id == english_id)
        result = await db_session.execute(stmt)

        english: Optional[English] = result.scalars().first()
        if not english:
            return None
        return english


class Suggestion(Base):
    __tablename__ = "suggestions"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)

    @staticmethod
    async def save(parent_id: int, child_id: int, db_session: Session):
        stmt = insert(Suggestion).values(
            parent=parent_id,
            child=child_id
        )
        await db_session.execute(stmt)

    @staticmethod
    async def delete(parent_id: int, child_id: int, db_session: Session):
        stmt = delete(Suggestion).where(
            and_(Suggestion.parent == parent_id, Suggestion.child == child_id))
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_parent(entry_id: int, db_session: Session) -> List['Entry']:
        stmt = select(Entry).filter(Suggestion.parent == entry_id, Entry.id == Suggestion.child)
        result = await db_session.execute(stmt)

        entries: List[Entry] = result.scalars().all()
        return entries

    @staticmethod
    async def retrieve_by_child(entry_id: int, db_session: Session) -> List['Entry']:
        stmt = select(Entry).filter(Suggestion.child == entry_id, Entry.id == Suggestion.parent)
        result = await db_session.execute(stmt)

        entries: List[Entry] = result.scalars().all()
        return entries


class Translation(Base):
    __tablename__ = "translations"

    parent = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    child = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                   primary_key=True)
    state = Column(Integer, ForeignKey('translation_states.id',
                                       ondelete="SET NULL"))

    @staticmethod
    async def save(parent_id: int, child_id: int, state_id: Optional[int], db_session: Session):
        stmt = insert(Translation).values(
            parent=parent_id,
            child=child_id,
            state=state_id
        )
        await db_session.execute(stmt)

    @staticmethod
    async def update(parent_id: int, child_id: int, state_id: Optional[int], db_session: Session):
        stmt = update(Translation).values(
            state=state_id
        ).where(Translation.parent == parent_id, Translation.child == child_id)
        await db_session.execute(stmt)

    @staticmethod
    async def delete(parent_id: int, db_session: Session):
        stmt = delete(Translation).where(Translation.parent == parent_id)
        await db_session.execute(stmt)

    # TODO: Maybe change this some time - currently two queries which could be inefficient
    @staticmethod
    async def retrieve_by_parent(parent_id: int, db_session: Session) -> (Optional['Entry'], Optional['TranslationState']):
        stmt_translation = select(Entry).where(Translation.parent == parent_id,
                                               Entry.id == Translation.child)
        result = await db_session.execute(stmt_translation)
        entry: Optional[Entry] = result.scalars().first()
        if not entry:
            return None, None

        stmt_state = select(TranslationState).where(Translation.parent == parent_id,
                                                    Translation.child == entry.id,
                                                    TranslationState.id == Translation.state)
        result = await db_session.execute(stmt_state)
        state: Optional[TranslationState] = result.scalars().first()

        return entry, state

    @staticmethod
    async def retrieve_by_child(child_id: int, db_session: Session) -> List['Entry']:
        stmt = select(Entry).filter(Translation.child == child_id, Entry.id == Translation.parent)
        result = await db_session.execute(stmt)

        entries: List[Entry] = result.scalars().first()
        return entries


class TranslationState(Base):
    __tablename__ = "translation_states"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)

    def __repr__(self):
        return f"Translation state[{self.id}]: {self.label}"

    async def save(self, db_session: Session):
        stmt = insert(TranslationState).values(
            label=self.label
        )
        result = await db_session.execute(stmt)
        await db_session.flush()
        self.id = result.inserted_primary_key[0]

    async def update(self, db_session: Session):
        stmt = update(TranslationState).values({
            "label": self.label
        }).where(TranslationState.id == self.id)

        result = await db_session.execute(stmt)
        return result.rowcount

    @staticmethod
    async def delete(state_id: int, db_session: Session):
        stmt = delete(TranslationState).where(TranslationState.id == state_id)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_id(state_id: int, db_session: Session) -> Optional['TranslationState']:
        stmt = select(TranslationState).where(TranslationState.id == state_id)
        result = await db_session.execute(stmt)

        state: Optional[TranslationState] = result.scalars().first()
        if not state:
            return None
        return state

    @staticmethod
    async def retrieve_all(filters: dict, db_session: Session) -> (List['TranslationState'], int):
        offset: int = filters.get('offset', 0)
        limit: int = filters.get('limit', LIMIT_SIZE)

        count_stmt = select(func.count(TranslationState.id))
        count_result = await db_session.execute(count_stmt)
        count = count_result.scalar()

        stmt = select(TranslationState).offset(offset).limit(limit)
        result = await db_session.execute(stmt)
        states: List[TranslationState] = result.scalars().all()

        return states, count


class Relation(Base):
    __tablename__ = "relations"

    entry1 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)
    entry2 = Column(Integer, ForeignKey('entries.id', ondelete="CASCADE"),
                    primary_key=True)

    @staticmethod
    async def save(entry1, entry2, db_session: Session):
        stmt = insert(Relation).values(
            entry1=entry1,
            entry2=entry2
        )
        await db_session.execute(stmt)

    @staticmethod
    async def delete(entry1: int, entry2: int, db_session: Session):
        stmt = delete(Relation).where(Relation.entry1 == entry1, Relation.entry2 == entry2)
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_by_entry1(entry1: int, db_session: Session) -> List['Entry']:
        stmt = select(Entry).filter(Relation.entry1 == entry1, Relation.entry2 == Entry.id)
        result = await db_session.execute(stmt)

        entries: List[Entry] = result.scalars().first()
        return entries

    @staticmethod
    async def retrieve_by_entry2(entry2: int, db_session: Session) -> List['Entry']:
        stmt = select(Entry).filter(Relation.entry2 == entry2, Relation.entry1 == Entry.id)
        result = await db_session.execute(stmt)

        entries: List[Entry] = result.scalars().first()
        return entries


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
        stmt = insert(Event).values(
            table=self.table,
            action=self.action,
            record_id=self.record_id,
            user_id=self.user_id,
            username=self.username
        )
        await db_session.execute(stmt)

    @staticmethod
    async def retrieve_all(filters: dict, db_session: Session) -> (List['Event'], int):
        count_stmt = select([func.count]).select_from(Event)
        count_result = await db_session.execute(count_stmt)
        count = count_result.scalar()

        offset: int = filters.get('offset', 0)
        limit: int = filters.get('limit', LIMIT_SIZE)

        stmt = select(Entry).order_by("time").offset(offset).limit(limit)

        result = await db_session.execute(stmt)
        entries = result.scalars().all()
        return entries, count
