from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas
from ..english_words import crud as english_crud


def get_link(db: Session, link_id: int, english_id: int) -> Optional[models.Link]:
    return db.query(models.Link).filter(models.Link.id == link_id, models.Link.english_entry_id == english_id).first()


def get_links(db: Session, pagination: Pagination, english_id: int) -> List[models.Link]:
    return db.query(models.Link).filter(models.Link.english_entry_id == english_id)\
        .offset(pagination.skip).limit(pagination.limit).all()


def create_link(db: Session, english_id: int, link: schemas.LinkBase) -> Optional[models.Link]:
    if english_crud.get_english_entry(db, english_id) is None:
        return None
    db_link = models.Link(
        title=link.title,
        url=link.url,
        english_entry_id=english_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def update_link(db: Session, updated_link: schemas.LinkPatch, english_id: int, link_id: int) -> Optional[models.Link]:
    link = get_link(db, link_id, english_id)
    if link is not None:
        if updated_link.url:
            link.url = updated_link.url
        if updated_link.title:
            link.title = updated_link.title
        db.commit()
    return link


def delete_link(db: Session, english_id: int, link_id: int) -> bool:
    link = db.query(models.Link).filter(models.Link.id == link_id, models.Link.english_entry_id == english_id)
    if link.first() is None:
        return False
    link.delete()
    db.commit()
    return True
