from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from dependencies import get_db, paginator, permissions
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[schemas.User])
def read_users(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    users = crud.get_users(db, pagination=pagination)
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


@router.patch('/{user_id}', response_model=schemas.User)
def change_user(user_id: int, user: schemas.UserPatch,
                current_user: schemas.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if current_user.permissions >= permissions.get('admin') or current_user.id == user_id:
        db_user = crud.update_user(db, user_id, user)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Uporabnik ne obstaja")
        return db_user
    else:
        raise HTTPException(status_code=403, detail="Nimate dovoljenja")


@router.delete('/{user_id}')
def delete_user(user_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.permissions >= permissions.get('admin') or current_user.id == user_id:
        if not crud.delete_user(db, user_id):
            raise HTTPException(status_code=404, detail="Uporabnik ne obstaja")
        return {"detail": "Izbris uspešen"}
    else:
        raise HTTPException(status_code=403, detail="Nimate dovoljenja")
