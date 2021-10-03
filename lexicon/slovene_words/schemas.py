from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SloveneEntryBase(BaseModel):
    lemma: str = Field(alias="word")
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True


class SloveneEntryCreate(SloveneEntryBase):
    pass


class SloveneEntryPatch(SloveneEntryBase):
    lemma: Optional[str] = Field(alias="word")
    alternative_gender_form: Optional[str] = Field(alias="alternative_form")


class SloveneEntry(SloveneEntryBase):
    id: int
    created: datetime = Field(alias="created_at")
    last_modified: datetime = Field(alias="edited_at", default=None)

    class Config:
        orm_mode = True


class SloveneEntryFull(SloveneEntry):
    alternative_gender_form: Optional[str] = Field(alias="alternative_form")
    #grammatical_position: str = Field(alias="type")

    class Config:
        orm_mode = True
