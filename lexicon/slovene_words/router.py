from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/slovene',
    tags=['slovene_entries']
)


@router.get('/', response_model=List[schemas.SloveneEntry])
def read_slovene_entries(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    entries = crud.get_slovene_entries(db, pagination)
    return entries


@router.post('/', response_model=schemas.SloveneEntryFull)
def create_slovene_entry(entry: schemas.SloveneEntryCreate, db: Session = Depends(get_db)):
    entry = crud.create_slovene_entry(db, entry)
    return entry


@router.get('/{slovene_id}', response_model=schemas.SloveneEntryFull)
def read_slovene_entry(slovene_id: int, db: Session = Depends(get_db)):
    entry = crud.get_slovene_entry(db, slovene_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return entry


@router.patch('/{slovene_id}', response_model=schemas.SloveneEntryFull)
def change_slovene_entry(slovene_id: int, entry: schemas.SloveneEntryPatch,
                         db: Session = Depends(get_db)):
    entry = crud.update_slovene_entry(db, slovene_id, entry)
    if not entry:
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return entry


@router.delete('/{slovene_id}')
def delete_slovene_entry(slovene_id: int, db: Session = Depends(get_db)):
    if not crud.delete_slovene_entry(db, slovene_id):
        raise HTTPException(status_code=404, detail="Beseda ne obstaja")
    return {"detail": "Izbris uspešen"}
