from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import crud, schemas

router = APIRouter(
    prefix='/english/{english_id}/related',
    tags=['related']
)


@router.get('/', response_model=List[schemas.Related])
def read_related_entries(english_id: int, db: Session = Depends(get_db)):
    related = crud.get_related(db, english_id)
    return related


@router.post('/')
def add_related_entry(english_id: int, word_id: int = -1, db: Session = Depends(get_db)):
    if word_id == -1:
        raise HTTPException(status_code=400, detail="Potreben podatek")
    english_entry = crud.create_related(db, english_id, word_id)
    if english_entry is None:
        raise HTTPException(status_code=400, detail="Ni uspelo")
    return {"detail": "Dodano"}


@router.delete('/')
def remove_related_entry(english_id: int, word_id: int = -1, db: Session = Depends(get_db)):
    crud.delete_related(db, english_id, word_id)
    return {"detail": "Odstranjeno"}
