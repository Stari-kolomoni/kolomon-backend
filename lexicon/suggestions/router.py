from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/{english_id}/suggestions',
    tags=['suggestions']
)


@router.get('/', response_model=List[schemas.Suggestion])
def read_suggestions(english_id: int, page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    suggestions = crud.get_suggestions(db, pagination, english_id)
    return suggestions


@router.post('/', response_model=schemas.Suggestion)
def create_suggestion(english_id: int, suggestion: schemas.SuggestionCreate, db: Session = Depends(get_db)):
    db_suggestion = crud.create_suggestion(db, english_id, suggestion)
    if db_suggestion is None:
        raise HTTPException(status_code=400, detail="Neveljavni podatki")
    return db_suggestion


@router.get('/{suggestion_id}', response_model=schemas.Suggestion)
def read_suggestion(english_id: int, suggestion_id: int, db: Session = Depends(get_db)):
    suggestion = crud.get_suggestion(db, suggestion_id, english_id)
    if suggestion is None:
        raise HTTPException(status_code=404, detail="Resurs ne obstaja")
    return suggestion


@router.patch('/{suggestion_id}', response_model=schemas.Suggestion)
def update_suggestion(english_id: int, suggestion_id: int,
                      suggestion: schemas.SuggestionPatch, db: Session = Depends(get_db)):
    suggestion = crud.update_suggestion(db, suggestion, suggestion_id, english_id)
    return suggestion


@router.delete('/{suggestion_id}')
def delete_suggestion(english_id: int, suggestion_id: int, db: Session = Depends(get_db)):
    if not crud.delete_suggestion(db, english_id, suggestion_id):
        raise HTTPException(status_code=404, detail="Resurs ne obstaja")
    return {"detail": "Izbris uspešen"}
