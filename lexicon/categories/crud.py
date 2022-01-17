from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session, pagination: Pagination) -> List[models.Category]:
    return db.query(models.Category).offset(pagination.skip).limit(pagination.limit).all()


def check_category_existence(db: Session, category: schemas.CategoryBase) -> bool:
    """Returns true, if category with these values exists"""
    res = db.query(models.Category) \
        .filter(and_(models.Category.name == category.name, models.Category.description == category.description)) \
        .first()

    if res is not None:
        return True
    return False


def create_category(db: Session, category: schemas.CategoryBase) -> Optional[models.Category]:
    db_category = models.Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int,
                    updated_category: schemas.CategoryPatch) -> Optional[models.Category]:
    category = get_category(db, category_id)
    if category is not None:
        if updated_category.name:
            category.name = updated_category.name
        if updated_category.description:
            category.description = updated_category.description
        db.commit()
    return category


def delete_category(db: Session, category_id: int) -> bool:
    category = db.query(models.Category).filter(models.Category.id == category_id)
    if not category.first():
        return False
    category.delete()
    db.commit()
    return True
