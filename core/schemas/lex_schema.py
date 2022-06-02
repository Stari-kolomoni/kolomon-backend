import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel

from core.models import lex_model as models


class TranslationState(BaseModel):
    id: int
    label: str

    @staticmethod
    def from_model(state_model: models.TranslationState):
        return TranslationState(
            id=state_model.id,
            label=state_model.label
        )


class EntryCreate(BaseModel):
    lemma: str
    description: Optional[str]
    language: Optional[str]
    additional_info: Optional[dict]

    def to_entry_instance(self) -> models.Entry:
        entry = models.Entry(
            lemma=self.lemma,
            description=self.description,
            language=self.language,
            extra_data=self.additional_info
        )
        return entry


class Entry(BaseModel):
    id: int
    lemma: str
    description: Optional[str]
    language: Optional[str]
    additional_info: Optional[dict]
    created: datetime.datetime
    edited: Optional[datetime.datetime]

    @staticmethod
    def from_model(model: models.Entry) -> 'Entry':
        entry = Entry(
            id=model.id,
            lemma=model.lemma,
            description=model.description,
            language=model.language,
            additional_info=model.extra_data,
            created=model.created,
            edited=model.modified
        )
        return entry

    @staticmethod
    def list_from_model(model_list: List[models.Entry]):
        entries = []
        for model in model_list:
            entries.append(Entry.from_model(model))
        return entries


class EntryList(BaseModel):
    entries: List[Entry]
    full_count: int


class EntryDetail(BaseModel):
    id: int
    lemma: str
    description: Optional[str]
    language: Optional[str]
    additional_info: Optional[dict]
    suggestions: List[Entry]
    translation: Optional[Entry]
    translation_state: Optional[TranslationState]
    created: datetime.datetime
    edited: Optional[datetime.datetime]

    @staticmethod
    def from_models(entry_model: models.Entry,
                    suggestions_model: List[models.Entry],
                    translation_model: Optional[models.Entry],
                    state_model: Optional[models.TranslationState]):
        suggestions = Entry.list_from_model(suggestions_model)

        translation = None
        if translation_model:
            translation = Entry.from_model(translation_model)
        state = None
        if state_model:
            state = TranslationState.from_model(state_model)

        entry = EntryDetail(
            id=entry_model.id,
            lemma=entry_model.lemma,
            description=entry_model.description,
            language=entry_model.language,
            additional_info=entry_model.extra_data,
            suggestions=suggestions,
            translation=translation,
            translation_state=state,
            created=entry_model.created,
            edited=entry_model.modified
        )
        return entry
