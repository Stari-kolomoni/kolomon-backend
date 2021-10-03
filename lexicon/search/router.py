from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator
from . import schemas, crud

router = APIRouter(
    prefix='/search',
    tags=['search']
)


@router.get('/quick')
def quick_search(page: int = 0, term: str = "", db: Session = Depends(get_db)):
    return {
        "detail": "V delu."
    }


@router.get('/full')
def full_search(page: int = 0, term: str = "", db: Session = Depends(get_db)):
    return {
        "detail": "V delu."
    }
