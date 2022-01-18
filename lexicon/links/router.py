from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db, paginator, GeneralBackendException, Message
from . import schemas, crud

router = APIRouter(
    prefix='/english/{english_id}/links',
    tags=['Links']
)


@router.get('/', response_model=List[schemas.Link], status_code=200)
def read_links(english_id: int, page: int = 0, db: Session = Depends(get_db)):
    pagination = paginator.paginate(page)
    suggestions = crud.get_links(db, pagination, english_id)
    return suggestions


@router.get('/{link_id}', response_model=schemas.Link, status_code=200,
            responses={404: {"model": Message, "description": "Link cannot be found"}})
def read_link(english_id: int, link_id: int, db: Session = Depends(get_db)):
    link = crud.get_link(db, link_id, english_id)
    if link is None:
        raise GeneralBackendException(404, "Link not found")
    return link


@router.post('/', response_model=schemas.Link, status_code=201,
             responses={400: {"model": Message, "description": "Link is not valid and/or cannot be inserted"}})
def create_link(english_id: int, link: schemas.LinkBase, db: Session = Depends(get_db)):
    """Note that all fields are required. If link title is empty string, url is used instead.
    Empty url results in exception."""
    db_link = crud.create_link(db, english_id, link)
    if db_link is None:
        raise GeneralBackendException(400, "Link not valid")
    return db_link


@router.patch('/{link_id}', response_model=schemas.Link, status_code=200,
              responses={404: {"model": Message, "description": "Link cannot be found and/or is not updatable"}})
def update_link(english_id: int, link_id: int, link: schemas.LinkPatch, db: Session = Depends(get_db)):
    link = crud.update_link(db, link, english_id, link_id)
    if link is None:
        raise GeneralBackendException(404, "Link not found")
    return link


@router.delete('/{link_id}', response_model=Message, status_code=200,
               responses={404: {"model": Message, "description": "Link cannot be found and/or is not deletable"}})
def delete_link(english_id: int, link_id: int, db: Session = Depends(get_db)):
    if not crud.delete_link(db, english_id, link_id):
        raise GeneralBackendException(404, "Link not found")
    return Message(message="Delete successful")
