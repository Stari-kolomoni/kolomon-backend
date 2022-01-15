from typing import Optional, List

from sqlalchemy.orm import Session

from pagination import Pagination
from .. import models
from . import schemas

from ..english_words import crud as english_crud
from ..slovene_words import crud as slovene_crud


def get_orphans(db: Session):
    db.execute("CREATE OR REPLACE VIEW entries_view AS"
               "(SELECT id, lemma, description, 'en' AS Type FROM english_entries)"
               "UNION ALL"
               "(SELECT id, lemma, description, 'sl' AS Type FROM slovene_entries)")
    result = ...
