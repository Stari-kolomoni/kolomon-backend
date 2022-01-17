from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='',
    tags=['other']
)


@router.get('/recent')
def read_recent_activity(count: int = 10, order_by: str = "any", db: Session = Depends(get_db)):
    return crud.get_recent(db, count, order_by)


@router.get('/orphans')
def read_orphans(count: int = 10, order_by: str = "random", db: Session = Depends(get_db)):
    return crud.get_orphans(db, count, order_by)
