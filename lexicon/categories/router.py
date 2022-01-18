from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, paginator, GeneralBackendException, Message
from . import schemas, crud

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)


@router.get('/', response_model=List[schemas.Category], status_code=200)
def read_categories(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    categories = crud.get_categories(db, pagination)
    return categories


@router.post('/', response_model=schemas.Category, status_code=201,
             responses={400: {"model": Message, "description": "Category already exists or cannot be created"}}
             )
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    exists = crud.check_category_existence(db, category)
    if exists:
        raise GeneralBackendException(400, "Category already exists")

    category = crud.create_category(db, category)
    if category is None:
        raise GeneralBackendException(400, "Category creation not possible")
    return category


@router.get('/{category_id}', response_model=schemas.Category, status_code=200,
            responses={404: {"model": Message, "description": "Category cannot be found"}}
            )
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise GeneralBackendException(404, "Category not found")
    return category


@router.patch('/{category_id}', response_model=schemas.Category, status_code=200,
              responses={404: {"model": Message, "description": "Category cannot be found or updated"}})
def change_category(category_id: int, category: schemas.CategoryPatch, db: Session = Depends(get_db)):
    category = crud.update_category(db, category_id, category)
    if category is None:
        raise GeneralBackendException(404, "Category not found or updatable")
    return category


@router.delete('/{category_id}', response_model=Message, status_code=200,
               responses={404: {"model": Message, "description": "Category cannot be found or deleted"}})
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, category_id):
        raise GeneralBackendException(404, "Category not found or deletable")
    msg = Message(message="Delete successful")
    return msg
