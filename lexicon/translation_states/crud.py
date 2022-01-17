from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas


def get_translation_states(db: Session, pagination: Pagination) -> List[schemas.TranslationState]:
    return db.query(models.TranslationState).offset(pagination.skip).limit(pagination.limit).all()


def get_translation_state(db: Session, state_id: int) -> schemas.TranslationState:
    return db.query(models.TranslationState).filter(models.TranslationState.id == state_id).first()


def create_translation_state(db: Session, state: schemas.TranslationStateBase) -> Optional[schemas.TranslationState]:
    db_entry = models.TranslationState(
        state=state.state
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_translation_state(db: Session, state: schemas.TranslationStateBase, state_id: int)\
        -> Optional[schemas.TranslationState]:
    entry = get_translation_state(db, state_id)
    if entry is not None:
        if state.state:
            entry.state = state.state
        db.commit()
    return entry


def delete_translation_state(db: Session, state_id: int) -> bool:
    entry = db.query(models.TranslationState).filter(models.TranslationState.id == state_id)
    if not entry.first():
        return False
    entry.delete()
    db.commit()
    return True
