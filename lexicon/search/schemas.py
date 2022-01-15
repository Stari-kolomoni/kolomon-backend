from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseSearchResult(BaseModel):
    id: int
    lemma: str = Field(alias="word")
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True


class QuickSearchResult(BaseSearchResult):
    language: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class EnglishSearchResult(BaseModel):
    en_id: int = Field(alias="id")
    en_lemma: str = Field(alias="word")
    en_description: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SloveneSearchResult(BaseModel):
    sl_id: int = Field(alias="id")
    sl_lemma: str = Field(alias="word")
    sl_description: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FullSearchResult(BaseModel):
    english: EnglishSearchResult
    slovene: SloveneSearchResult

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
