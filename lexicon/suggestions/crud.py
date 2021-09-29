from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from pagination import Pagination
from .. import models
from . import schemas
from ..english_words import crud as english_crud


def get_suggestion(db: Session, suggestion_id: int, english_id: int) -> Optional[models.Suggestion]:
    english_entry = db.query(models.EnglishEntry).filter(models.EnglishEntry.id == english_id).first()
    if english_entry is None:
        return None
    return english_entry.suggested_translations.filter(models.Suggestion.id == suggestion_id).first()


def get_suggestions(db: Session, pagination: Pagination, english_id: int) -> List[models.Suggestion]:
    return db.query(models.Suggestion).filter(models.Suggestion.english_entry_id == english_id)\
        .offset(pagination.skip).limit(pagination.limit).all()


def create_suggestion(db: Session, english_id: int, suggestion: schemas.SuggestionCreate)\
        -> Optional[models.Suggestion]:
    if english_crud.get_english_entry(db, english_id) is None:
        return None
    separate_gender_form = False
    if suggestion.separate_gender_form:
        separate_gender_form = suggestion.separate_gender_form
    db_suggestion = models.Suggestion(
        lemma=suggestion.lemma,
        description=suggestion.description,
        separate_gender_form=separate_gender_form,
        english_entry_id=english_id
    )
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion


def update_suggestion(db: Session, updated_suggestion: schemas.SuggestionPatch, suggestion_id: int, english_id: int)\
        -> Optional[schemas.Suggestion]:
    suggestion = get_suggestion(db, suggestion_id, english_id)
    if suggestion is not None:
        if updated_suggestion.lemma:
            suggestion.lemma = updated_suggestion.lemma
        if updated_suggestion.description:
            suggestion.description = updated_suggestion.description
        if updated_suggestion.separate_gender_form is not None:
            suggestion.separate_gender_form = updated_suggestion.separate_gender_form
        db.commit()
    return suggestion


def delete_suggestion(db: Session, english_id: int, suggestion_id: int) -> bool:
    english_entry = db.query(models.EnglishEntry).filter(models.EnglishEntry.id == english_id).first() \
        .options(joinedload(models.EnglishEntry.suggested_translations))
    suggestion = english_entry.suggested_translations.filter(models.Suggestion.id == suggestion_id)
    if not suggestion.first():
        return False
    suggestion.delete()
    db.commit()
    return True
