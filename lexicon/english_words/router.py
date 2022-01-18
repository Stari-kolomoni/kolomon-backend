from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, paginator, GeneralBackendException, Message
from . import schemas, crud

router = APIRouter(
    prefix='/english',
    tags=['English entries']
)


@router.get('/', response_model=List[schemas.EnglishEntry], status_code=200)
def read_english_entries(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    entries = crud.get_english_entries(db, pagination)
    return entries


@router.post('/', response_model=schemas.EnglishEntry, status_code=201,
             responses={400: {"model": Message}})
def create_english_entry(entry: schemas.EnglishEntryBase, db: Session = Depends(get_db)):
    entry = crud.create_english_entry(db, entry)
    if entry is None:
        raise GeneralBackendException(400, "Data invalid")
    return entry


@router.get('/{english_id}', response_model=schemas.EnglishEntryFull, status_code=200,
            responses={404: {"model": Message}})
def read_english_entry(english_id: int, db: Session = Depends(get_db)):
    entry = crud.get_english_entry(db, english_id)
    if not entry:
        raise GeneralBackendException(404, "Entry not found")
    return entry


@router.patch('/{english_id}', response_model=schemas.EnglishEntry, status_code=200,
              responses={404: {"model": Message}})
def change_english_entry(english_id: int, entry: schemas.EnglishEntryPatch, db: Session = Depends(get_db)):
    entry = crud.update_english_entry(db, english_id, entry)
    if not entry:
        raise GeneralBackendException(404, "Entry not found")
    return entry


@router.delete('/{english_id}', response_model=Message, status_code=200,
               responses={404: {"model": Message}})
def delete_english_entry(english_id: int, db: Session = Depends(get_db)):
    if not crud.delete_english_entry(db, english_id):
        raise GeneralBackendException(404, "Entry not found")
    msg = Message(message="Delete successful")
    return msg
