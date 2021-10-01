from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas


def get_slovene_entries(db: Session, pagination: Pagination) -> List[models.SloveneEntry]:
    return db.query(models.SloveneEntry).offset(pagination.skip).limit(pagination.limit).all()


def get_slovene_entry(db: Session, slovene_id: int) -> Optional[models.SloveneEntry]:
    return db.query(models.SloveneEntry).filter(models.SloveneEntry.id == slovene_id).first()


def create_slovene_entry(db: Session, slovene: schemas.SloveneEntryCreate) -> Optional[models.SloveneEntry]:
    db_entry = models.SloveneEntry(
        lemma=slovene.lemma,
        description=slovene.description
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_slovene_entry(db: Session, slovene_id: int,
                         updated_entry: schemas.SloveneEntryPatch) -> Optional[models.SloveneEntry]:
    entry = get_slovene_entry(db, slovene_id)
    if entry is not None:
        if updated_entry.lemma:
            entry.lemma = updated_entry.lemma
        if updated_entry.description:
            entry.description = updated_entry.description
        if updated_entry.alternative_gender_form:
            entry.alternative_gender_form = updated_entry.alternative_gender_form
        db.commit()
    return entry


def delete_slovene_entry(db: Session, slovene_id: int) -> bool:
    entry = db.query(models.SloveneEntry).filter(models.SloveneEntry.id == slovene_id)
    if not entry.first():
        return False
    entry.delete()
    db.commit()
    return True
