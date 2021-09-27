from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .. import models
from ..categories import schemas as category_schemas


class EnglishEntryBase(BaseModel):
    lemma: str = Field(alias="word")
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True


class EnglishEntryCreate(EnglishEntryBase):

    class Config:
        allow_population_by_field_name = True


class EnglishEntryPatch(EnglishEntryBase):
    lemma: Optional[str] = Field(alias="word")


class EnglishEntry(EnglishEntryBase):
    id: int
    translation_state_id: int = Field(alias="translation_state", default=None)
    created: datetime = Field(alias="created_at")
    last_modified: datetime = Field(alias="edited_at", default=None)

    class Config:
        orm_mode = True


class EnglishEntryFull(EnglishEntry):
    translation_comment: Optional[str]
    edited_by_id = Optional[int]
    edited_by_name = Optional[str]

    categories = List[category_schemas.Category]

    class Config:
        arbitrary_types_allowed = True
