from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Table, Boolean, Index, DDL, event
from sqlalchemy.orm import relationship

from database import Base
from db.TsVector import TsVector

category2english = Table(
    'category2english', Base.metadata,
    Column('category_id', ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True),
    Column('english_id', ForeignKey('english_entries.id', ondelete="CASCADE"), primary_key=True)
)

english2english = Table(
    'english2english', Base.metadata,
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
    links = relationship("Link", back_populates="english_entry")
    suggested_translations = relationship("Suggestion", back_populates="english_entry", lazy='dynamic')

    created = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())

    #tsvector = Column(TsVector)

    #__table_args__ = (Index('tsvector_idx', 'tsvector', postgresql_using='gin'),)


class SloveneEntry(Base):
    __tablename__ = "slovene_entries"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    lemma = Column(String)
    description = Column(String, nullable=True)

    alternative_gender_form = Column(String, nullable=True)
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
    english_entry_id = Column(Integer, ForeignKey('english_entries.id', ondelete="CASCADE"))
    english_entry = relationship("EnglishEntry", back_populates="suggested_translations")

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

    english_entry_id = Column(Integer, ForeignKey('english_entries.id', ondelete="CASCADE"))
    english_entry = relationship("EnglishEntry", back_populates="links")


#trigger_snippet = DDL("""
#CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
#ON english_entries
#FOR EACH ROW EXECUTE PROCEDURE
#tsvector_update_trigger(tsvector, 'pg_catalog.english', 'details')
#""")

#event.listen(EnglishEntry.__table__, 'after_create', trigger_snippet.execute_if(dialect='postgresql'))
