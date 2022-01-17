from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TranslationStateBase(BaseModel):
    state: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TranslationState(TranslationStateBase):
    state_id: int
