from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/english',
    tags=['english_entries']
)


@router.get('/', response_model=List[schemas.EnglishEntry])
def read_english_entries(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    entries = crud.get_english_entries(db, pagination)
    return entries


@router.post('/', response_model=schemas.EnglishEntry)
def create_english_entry(entry: schemas.EnglishEntryCreate, db: Session = Depends(get_db)):
    entry = crud.create_english_entry(db, entry)
    return entry
