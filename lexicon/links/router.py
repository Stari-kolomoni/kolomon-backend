from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator, GeneralBackendException
from . import schemas, crud

router = APIRouter(
    prefix='/english/{english_id}/links',
    tags=['links']
)


@router.get('/', response_model=List[schemas.Link], status_code=200,
            )
def read_links(english_id: int, page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    suggestions = crud.get_links(db, pagination, english_id)
    return suggestions


@router.get('/{link_id}', response_model=schemas.Link)
def read_link(english_id: int, link_id: int, db: Session = Depends(get_db)):
    link = crud.get_link(db, link_id, english_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Resurs ne obstaja")
    return link


@router.post('/', response_model=schemas.Link)
def create_link(english_id: int, link: schemas.LinkBase, db: Session = Depends(get_db)):
    db_link = crud.create_link(db, english_id, link)
    if db_link is None:
        raise HTTPException(status_code=400, detail="Neveljavni podatki")
    return db_link


@router.patch('/{link_id}', response_model=schemas.Link)
def update_link(english_id: int, link_id: int, link: schemas.LinkPatch, db: Session = Depends(get_db)):
    link = crud.update_link(db, link, english_id, link_id)
    return link


@router.delete('/{link_id}')
def delete_link(english_id: int, link_id: int, db: Session = Depends(get_db)):
    if not crud.delete_link(db, english_id, link_id):
        raise HTTPException(status_code=404, detail="Resurs ne obstaja")
    return {"detail": "Izbris uspešen"}
