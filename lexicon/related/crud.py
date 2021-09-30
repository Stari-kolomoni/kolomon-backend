from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas
from ..english_words import crud as english_crud


def get_related(db: Session, english_id: int):
    entry = db.query(models.EnglishEntry).filter(models.EnglishEntry.id == english_id).first()
    related = entry.related
    return related


def create_related(db: Session, english_id: int, related_id: int):
    related_entry = english_crud.get_english_entry(db, related_id)
    english_entry = english_crud.get_english_entry(db, english_id)
    if related_entry is None or english_entry is None:
        return None

    english_entry.related.append(related_entry)
    db.commit()
    return english_entry


def delete_related(db: Session, english_id: int, related_id: int):
    related_entry = english_crud.get_english_entry(db, related_id)
    english_entry = english_crud.get_english_entry(db, english_id)
    if related_entry is None or english_entry is None:
        return None
    english_entry.related.remove(related_entry)
    db.commit()
