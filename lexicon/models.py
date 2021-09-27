from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from database import Base

category2english = Table(
    'category2english', Base.metadata,
    Column('category_id', ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True),
    Column('english_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True)
)

link2english = Table(
    'link2english', Base.metadata,
    Column('link_id', ForeignKey('links.id', ondelete="CASCADE"), primary_key=True),
    Column('english_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True)
)

suggestion2english = Table(
    'suggestion2english', Base.metadata,
    Column('suggestion_id', ForeignKey('suggested_translations.id', ondelete="CASCADE"), primary_key=True),
    Column('english_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True)
)

english2english = Table(
    'entry2entry', Base.metadata,
    Column('left_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True),
    Column('right_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True)
)

slovene2slovene = Table(
    'slovene2slovene', Base.metadata,
    Column('left_id', ForeignKey('slovene_entries.id', ondelete="CASCADE"), primary_key=True),
    Column('right_id', ForeignKey('slovene_entries.id', ondelete="CASCADE"), primary_key=True)
)


class EnglishEntry(Base):
    __tablename__ = "english_entries"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    lemma = Column(String)
    description = Column(String, nullable=True)

    translation_state_id = Column(Integer, ForeignKey('translation_states.id'), nullable=True)
    translation_comment = Column(String, nullable=True)
    translation_id = Column(Integer, ForeignKey('slovene_entries.id'), nullable=True)
    translation = relationship("SloveneEntry", back_populates='english_entry')

    related = relationship("EnglishEntry", secondary=english2english,
                           primaryjoin=id == english2english.c.left_id,
                           secondaryjoin=id == english2english.c.right_id)
    categories = relationship("Category", secondary=category2english)
    links = relationship("Link", secondary=link2english)
    suggested_translations = relationship("Suggestion", secondary=suggestion2english)

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())


class SloveneEntry(Base):
    __tablename__ = "slovene_entries"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    lemma = Column(String)
    description = Column(String, nullable=True)

    alternative_gender_form = Column(String, nullable=True)
    grammatical_position = Column(String)
    related = relationship("SloveneEntry", secondary=slovene2slovene,
                           primaryjoin=id == slovene2slovene.c.left_id,
                           secondaryjoin=id == slovene2slovene.c.right_id)
    english_entry = relationship("EnglishEntry", back_populates="translation")

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())


class Suggestion(Base):
    __tablename__ = "suggested_translations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    lemma = Column(String)
    separate_gender_form = Column(Boolean)
    description = Column(String, nullable=True)

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)


class TranslationState(Base):
    __tablename__ = "translation_states"

    id = Column(Integer, autoincrement=True, primary_key=True)
    state = Column(String)


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    url = Column(String)
