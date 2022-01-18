from typing import Optional, List

from sqlalchemy import or_, text
from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas
from ..english_words import crud as english_crud


def get_related(db: Session, english_id: int) -> List[schemas.Related]:
    sql = """
            
        """
    parsed_sql = text(sql)
    return db.execute(parsed_sql, {"id": english_id}).all()


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
