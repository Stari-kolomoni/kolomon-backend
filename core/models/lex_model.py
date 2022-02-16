from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base
import core.schemas.lex_schema as ls


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    lemma = Column(String, index=True)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, onupdate=func.now(), nullable=True)

    categories = relationship('Category', secondary='category_to_entry',
                              back_populates='entries')

    __mapper__args = {'eager_defaults': True}

    @staticmethod
    def from_schema(entry_scheme: ls.EntryCreate):
        if entry_scheme.lemma == "":
            return None

        entry = Entry(
            lemma=entry_scheme.lemma,
            description=entry_scheme.description,
            language=entry_scheme.language
        )
        return entry


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    url = Column(String, index=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))

    @staticmethod
    def from_schema_from_id(link_scheme: ls.LinkCreate, entry_id):
        if link_scheme.url == "":
            return None
        link = Link(
            title=link_scheme.title,
            url=link_scheme.url,
            entry_id=entry_id
        )
        return link


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    entries = relationship('Entry', secondary='category_to_entry',
                           back_populates='categories')


class Slovene(Base):
    __tablename__ = "slovene"

    id = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    alt_form = Column(String, nullable=True)


class English(Base):
    __tablename__ = "english"

    id = Column(Integer, ForeignKey('entries.id'), primary_key=True)


class Suggestion(Base):
    __tablename__ = "suggestions"

    parent = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    child = Column(Integer, ForeignKey('entries.id'), primary_key=True)


class Translation(Base):
    __tablename__ = "translations"

    parent = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    child = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    state = Column(Integer, ForeignKey('translation_states.id'))


class TranslationState(Base):
    __tablename__ = "translation_states"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)


class Relation(Base):
    __tablename__ = "relations"

    entry1 = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    entry2 = Column(Integer, ForeignKey('entries.id'), primary_key=True)


class CategoryToEntry(Base):
    __tablename__ = "category_to_entry"

    entry_id = Column(Integer, ForeignKey('entries.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    table = Column(String)
    action = Column(String)
    record_id = Column(Integer)
    user_id = Column(Integer)
    username = Column(String)
    time = Column(DateTime, server_default=func.now())
