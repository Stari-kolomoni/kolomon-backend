from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud
from ..suggestions import router as suggestion_router

router = APIRouter(
    prefix='/english',
    tags=['english_entries']
)

router.include_router(suggestion_router.router)


@router.get('/', response_model=List[schemas.EnglishEntry])
def read_english_entries(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    entries = crud.get_english_entries(db, pagination)
    return entries


@router.post('/', response_model=schemas.EnglishEntry)
def create_english_entry(entry: schemas.EnglishEntryCreate, db: Session = Depends(get_db)):
    entry = crud.create_english_entry(db, entry)
    return entry


@router.get('/{english_id}', response_model=schemas.EnglishEntryFull)
def read_english_entry(english_id: int, db: Session = Depends(get_db)):
    entry = crud.get_english_entry(db, english_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return entry


@router.patch('/{english_id}', response_model=schemas.EnglishEntry)
def change_english_entry(english_id: int, entry: schemas.EnglishEntryPatch, db: Session = Depends(get_db)):
    entry = crud.update_english_entry(db, english_id, entry)
    if not entry:
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return entry


@router.delete('/{english_id}')
def delete_english_entry(english_id: int, db: Session = Depends(get_db)):
    if not crud.delete_english_entry(db, english_id):
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return {"detail": "Izbris uspešen"}
