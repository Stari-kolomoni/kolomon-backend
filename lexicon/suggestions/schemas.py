from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class SuggestionBase(BaseModel):
    lemma: str = Field(alias="suggestion")
    description: Optional[str] = Field(alias="comment", default=None)
    separate_gender_form: Optional[bool]

    class Config:
        allow_population_by_field_name = True


class SuggestionCreate(SuggestionBase):
    pass


class SuggestionPatch(SuggestionBase):
    english_entry_id: int = Field(alias="english_entry")


class Suggestion(SuggestionBase):
    id: int
    created: datetime = Field(alias="created_at")
    last_modified: datetime = Field(alias="edited_at", default=None)
    separate_gender_form: bool

    class Config:
        orm_mode = True
