from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas


def get_english_entries(db: Session, pagination: Pagination) -> List[models.EnglishEntry]:
    return db.query(models.EnglishEntry).offset(pagination.skip).limit(pagination.limit).all()


def get_english_entry(db: Session, entry_id: int) -> Optional[models.EnglishEntry]:
    return db.query(models.EnglishEntry).filter(models.EnglishEntry.id == entry_id).first()


def create_english_entry(db: Session, entry: schemas.EnglishEntryCreate) -> Optional[models.Category]:
    db_entry = models.EnglishEntry(
        lemma=entry.lemma,
        description=entry.description
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_english_entry(db: Session, entry_id: int,
                         updated_entry: schemas.EnglishEntryPatch) -> Optional[models.EnglishEntry]:
    entry = get_english_entry(db, entry_id)
    if entry is not None:
        if updated_entry.lemma:
            entry.lemma = updated_entry.lemma
        if updated_entry.description:
            entry.description = updated_entry.description
        db.commit()
    return entry


def delete_english_entry(db: Session, entry_id: int) -> bool:
    entry = db.query(models.EnglishEntry).filter(models.EnglishEntry.id == entry_id)
    if not entry.first():
        return False
    entry.delete()
    db.commit()
    return True


def get_slovene_translation(db: Session, entry_id: int) -> Optional[models.SloveneEntry]:
    english_entry = get_english_entry(db, entry_id)
    if english_entry is not None:
        return english_entry.translation
    return english_entry

