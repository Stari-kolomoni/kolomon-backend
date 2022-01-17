from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas

from ..english_words import crud as english_crud
from ..slovene_words import crud as slovene_crud


def get_orphans(db: Session, count: int, order: str) -> List[schemas.Recent]:
    sql = """
        (SELECT en.id, en.lemma, en.description, 'en' AS language
            FROM english_entries AS en
            WHERE en.translation_id IS NULL
        UNION
            SELECT sl.id, sl.lemma, sl.description, 'sl' AS language
            FROM slovene_entries AS sl
            LEFT JOIN english_entries AS en1 ON sl.id = en1.translation_id
            WHERE en1.translation_id IS NULL
        LIMIT :count)
    """
    if order == 'alphabetical':
        sql += "\nORDER BY lemma ASC"

    return db.execute(sql, {"count": count}).all()


def get_recent(db: Session, count: int, order: str) -> List[schemas.Recent]:
    sql = """
        (SELECT en.id, en.lemma, en.description, 'en' AS language, en.created, en.last_modified
        FROM english_entries AS en
        UNION
        SELECT sl.id, sl.lemma, sl.description, 'sl' AS language, sl.created, sl.last_modified
        FROM slovene_entries AS sl)
    """
    if order == 'created':
        sql += "\nORDER BY created DESC"
    if order == 'edits':
        sql += "\nORDER BY last_modified DESC"

    sql += "\nLIMIT :limit"

    return db.execute(sql, {"limit": count}).all()
