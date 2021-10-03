from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseSearchResult(BaseModel):
    id: int
    word: str
    description: str


class QuickSearchResult(BaseSearchResult):
    language: str


class FullSearchResult(BaseModel):
    english: BaseSearchResult
    slovene: BaseSearchResult
