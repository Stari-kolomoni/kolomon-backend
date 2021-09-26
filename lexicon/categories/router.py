from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.get('/', response_model=List[schemas.Category])
def read_categories(page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    categories = crud.get_categories(db, pagination)
    return categories


@router.post('/', response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = crud.create_category(db, category)
    return category


@router.get('/{category_id}', response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Kategorija ne obstaja")
    return category


@router.patch('/{category_id}', response_model=schemas.Category)
def change_category(category_id: int, category: schemas.CategoryPatch, db: Session = Depends(get_db)):
    category = crud.update_category(db, category_id, category)
    if category is None:
        raise HTTPException(status_code=404, detail="Kategorija ne obstaja")
    return category


@router.delete('/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Kategorija ne obstaja")
    return {"detail": "Izbris uspešen"}
