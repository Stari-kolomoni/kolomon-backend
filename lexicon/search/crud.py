from typing import List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from pagination import Pagination
from .. import models
from . import schemas


def get_search_quick(db: Session, pagination: Pagination, term: str) -> List[schemas.QuickSearchResult]:
    en = models.EnglishEntry
    s1 = select([en.id, en.lemma, en.description]).filter(en.lemma.ilike('%' + term + '%'))\
        .add_columns(bindparam('lang', 'en').label('language'))

    sl = models.SloveneEntry
    s2 = select([sl.id, sl.lemma, sl.description]).filter(sl.lemma.ilike('%' + term + '%'))\
        .add_columns(bindparam('lang', 'sl').label('language'))

    q = s1.union(s2).subquery()
    return db.query(q).offset(pagination.skip).limit(pagination.limit).all()


def get_search_full(db: Session, pagination: Pagination, term: str) -> List[schemas.FullSearchResult]:
    sql = """
        SELECT en.id AS en_id, en.lemma AS en_lemma, en.description AS en_description,
            sl.id AS sl_id, sl.lemma AS sl_lemma, sl.description AS sl_description
            FROM english_entries en
        FULL OUTER JOIN slovene_entries sl ON en.translation_id = sl.id
            WHERE en.lemma ILIKE :term OR en.description ILIKE :term
            OR sl.lemma ILIKE :term OR sl.description ILIKE :term
            LIMIT :limit OFFSET :offset
    """
    term = '%' + term + '%'
    return db.execute(sql, {"term": term, "limit": pagination.limit, "offset": pagination.skip}).all()
