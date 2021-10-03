from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas


def get_search_quick(db: Session, pagination: Pagination, term: str) -> List[schemas.QuickSearchResult]:
    pass


def get_search_full(db: Session, pagination: Pagination, term: str) -> List[schemas.FullSearchResult]:
    pass

