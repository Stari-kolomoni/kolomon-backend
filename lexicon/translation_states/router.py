from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/translation_states',
    tags=['Translation States']
)


@router.get('/')
def read_translation_states(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    return crud.get_translation_states(db, pagination)


@router.get('/{state_id}')
def read_translation_state(state_id: int, db: Session = Depends(get_db)):
    return crud.get_translation_state(db, state_id)


@router.post('/')
def create_translation_state(state: schemas.TranslationStateBase, db: Session = Depends(get_db)):
    return crud.create_translation_state(db, state)


@router.patch('/{state_id}')
def patch_translation_state(state: schemas.TranslationStateBase, state_id: int, db: Session = Depends(get_db)):
    return crud.update_translation_state(db, state, state_id)


@router.delete('/{state_id}')
def delete_translation_state(state_id: int, db: Session = Depends(get_db)):
    return crud.delete_translation_state(db, state_id)
