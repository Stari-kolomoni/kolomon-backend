from pydantic import BaseModel


class EntryCreate(BaseModel):
    lemma: str
    description: str
    language: str
