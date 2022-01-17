from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Recent(BaseModel):
    word_id: int
    word_name: str
    time: datetime
    user_id: int
    user_name: str
    pass

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Orphans(BaseModel):
    id: int
    language: str
    word: str = Field(alias="lemma")
    description: str

    class Config:
        orm_mode = True
        #allow_population_by_field_name = True
