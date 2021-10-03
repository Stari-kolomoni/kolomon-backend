from typing import Optional, List

from sqlalchemy.orm import Session

from .. import models
from ..slovene_words import schemas as slovene_schemas
from ..slovene_words import crud as slovene_crud
from ..english_words import schemas as english_schemas
from ..english_words import crud as english_crud


def get_slovene_translation(db: Session, entry_id: int) -> Optional[models.SloveneEntry]:
    english_entry = english_crud.get_english_entry(db, entry_id)
    if english_entry is not None:
        return english_entry.translation
    return english_entry


def add_slovene_translation(db: Session, english_id: int, slovene_id: int) -> bool:
    english_entry = english_crud.get_english_entry(db, english_id)
    slovene_entry = slovene_crud.get_slovene_entry(db, slovene_id)
    if english_entry is not None and slovene_entry is not None:
        english_entry.translation = slovene_entry
        db.commit()
        return True
    return False
