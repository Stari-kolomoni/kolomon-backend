from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from users import models, schemas, auth


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, pagination: Pagination) -> List[models.User]:
    return db.query(models.User).offset(pagination.skip).limit(pagination.limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> Optional[models.User]:
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        permissions=user.permissions,
        joined=datetime.utcnow(),
        last_active=datetime.utcnow(),
        is_active=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserPatch) -> Optional[models.User]:
    user = get_user(db, user_id)
    if user is None:
        return user
    if user_update.permissions:
        user.permissions = user_update.permissions
    if user_update.password:
        user.hashed_password = auth.get_password_hash(user_update.password)
    db.commit()
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        return False
    user.delete()
    db.commit()
    return True
