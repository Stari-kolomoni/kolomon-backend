import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel


class EventCreate(BaseModel):
    table: str
    action: str
    record_id: int
    user_id: int
    username: str


class LinkCreate(BaseModel):
    title: Optional[str]
    url: str


class EntryCreate(BaseModel):
    lemma: str
    description: Optional[str]
    language: Optional[str]
    additional_info: Optional[Dict[str, str]]


class Link(BaseModel):
    id: int
    title: Optional[str]
    url: str

    @staticmethod
    def from_sql(link_row):
        link = Link(
            id=link_row[0],
            title=link_row[1],
            url=link_row[2]
        )
        return link


class TranslationState(BaseModel):
    id: int
    label: str


class EntryMinimal(BaseModel):
    id: int
    lemma: str
    description: Optional[str]
    language: Optional[str]

    @staticmethod
    def from_sql(entry_row):
        entry = EntryMinimal(
            id=entry_row[0],
            lemma=entry_row[1],
            description=entry_row[2],
            language=entry_row[3]
        )
        return entry


class EntryUpdate(BaseModel):
    lemma: str
    description: str


class Entry(BaseModel):
    id: int
    lemma: str
    description: Optional[str]
    language: Optional[str]
    created: datetime.datetime
    edited: Optional[datetime.datetime]
    suggestions: List[EntryMinimal]
    relations: List[EntryMinimal]
    links: List[Link]

    @staticmethod
    def from_sql(entry_row):
        entry = Entry(
            id=entry_row[0],
            lemma=entry_row[1],
            description=entry_row[2],
            language=entry_row[3],
            created=entry_row[4],
            edited=entry_row[5],
            suggestions=[],
            relations=[],
            links=[]
        )
        return entry


class EntryPair(BaseModel):
    original: Entry
    translation: Optional[Entry]
    translation_state: Optional[TranslationState]
