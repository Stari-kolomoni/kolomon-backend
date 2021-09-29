from typing import Optional

from pydantic import BaseModel, Field


class LinkBase(BaseModel):
    title: str
    url: str

    class Config:
        allow_population_by_field_name = True


class LinkCreate(LinkBase):
    pass


class LinkPatch(LinkBase):
    title: Optional[str]
    url: Optional[str]


class Link(LinkBase):
    id: int

    class Config:
        orm_mode = True
