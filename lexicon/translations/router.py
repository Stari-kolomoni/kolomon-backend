from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import crud
from ..slovene_words import schemas as slovene_schemas

router = APIRouter(
    prefix='/english/{english_id}/translation',
    tags=['translation']
)


@router.get('/', response_model=slovene_schemas.SloveneEntryFull)
def read_slovene_translation(english_id: int, db: Session = Depends(get_db)):
    entry = crud.get_slovene_translation(db, english_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return entry


@router.post('/')
def link_slovene_to_english(english_id: int, slovene_id: int = -1, db: Session = Depends(get_db)):
    if slovene_id < 1:
        raise HTTPException(status_code=400, detail="ID slovenske besede ni veljaven")
    if not crud.add_slovene_translation(db, english_id, slovene_id):
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return {
        "detail": "Povezava uspela"
    }
