from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas, auth
from dependencies import get_db,  oauth2_request_form
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Uporabniško ime je že zavzeto")
    return crud.create_user(db, user)


@router.get('/me', response_model=schemas.User)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Uporabnik ne obstaja")
    return db_user


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="Uporabnik ne obstaja")
    return {"message": "Izbris uspešen"}
