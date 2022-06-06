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

    @staticmethod
    def list_from_model(states_model: List[models.TranslationState]) -> List['TranslationState']:
        schema_list: List[TranslationState] = []
        for model in states_model:
            schema_list.append(TranslationState.from_model(model))
        return schema_list


class TranslationStateList(BaseModel):
    translation_states: List[TranslationState]
    full_count: int


class TranslationStateCreate(BaseModel):
    label: str

    def to_state_instance(self) -> models.TranslationState:
        state = models.TranslationState(
            label=self.label
        )
        return state


class Link(BaseModel):
    id: int
    title: Optional[str]
    url: str

    @staticmethod
    def from_model(link_model: models.Link) -> 'Link':
        return Link(
            id=link_model.id,
            title=link_model.title,
            url=link_model.url
        )

    @staticmethod
    def list_from_model(links_model: List[models.Link]):
        schema_list: List[Link] = []
        for model in links_model:
            schema_list.append(Link.from_model(model))
        return schema_list


class LinkCreate(BaseModel):
    title: Optional[str]
    url: str

    def to_link_instance(self, entry_id: int) -> models.Link:
        link = models.Link(
            title=self.title,
            url=self.url,
            entry_id=entry_id
        )
        return link


class Category(BaseModel):
    id: int
    name: str
    description: Optional[str]

    @staticmethod
    def from_model(category_model: models.Category):
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description
        )

    @staticmethod
    def list_from_model(categories_model: List[models.Category]):
        schema_list: List[Category] = []
        for model in categories_model:
            schema_list.append(Category.from_model(model))
        return schema_list


class CategoryList(BaseModel):
    categories: List[Category]
    full_count: int


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]

    def to_category_instance(self) -> models.Category:
        return models.Category(
            name=self.name,
            description=self.description
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


class EntryUpdate(BaseModel):
    lemma: str
    description: Optional[str]
    additional_info: Optional[dict]

    def to_model(self, entry_id: int) -> models.Entry:
        entry = models.Entry(
            id=entry_id,
            lemma=self.lemma,
            description=self.description,
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


class EntryMinimal(BaseModel):
    id: int
    lemma: str
    created: datetime.datetime
    edited: Optional[datetime.datetime]

    @staticmethod
    def from_model(model: models.Entry) -> 'EntryMinimal':
        entry = EntryMinimal(
            id=model.id,
            lemma=model.lemma,
            created=model.created,
            edited=model.modified
        )
        return entry

    @staticmethod
    def list_from_model(model_list: List[models.Entry]) -> List['EntryMinimal']:
        entries = []
        for model in model_list:
            entries.append(EntryMinimal.from_model(model))
        return entries


class EntryDetail(BaseModel):
    id: int
    lemma: str
    description: Optional[str]
    language: Optional[str]
    additional_info: Optional[dict]

    suggestions: List[Entry]
    translation: Optional[Entry]
    translation_state: Optional[TranslationState]
    links: List[Link]
    related_entries: List[EntryMinimal]
    categories: List[Category]

    created: datetime.datetime
    edited: Optional[datetime.datetime]

    @staticmethod
    def from_models(entry_model: models.Entry,
                    suggestions_model: List[models.Entry],
                    translation_model: Optional[models.Entry],
                    state_model: Optional[models.TranslationState],
                    links_model: List[models.Link],
                    related_entries_model: List[models.Entry],
                    categories_model: List[models.Category]):

        suggestions = Entry.list_from_model(suggestions_model)

        translation = None
        if translation_model:
            translation = Entry.from_model(translation_model)
        state = None
        if state_model:
            state = TranslationState.from_model(state_model)

        links = Link.list_from_model(links_model)

        related_entries = EntryMinimal.list_from_model(related_entries_model)

        categories = Category.list_from_model(categories_model)

        entry = EntryDetail(
            id=entry_model.id,
            lemma=entry_model.lemma,
            description=entry_model.description,
            language=entry_model.language,
            additional_info=entry_model.extra_data,

            suggestions=suggestions,
            translation=translation,
            translation_state=state,
            links=links,
            related_entries=related_entries,
            categories=categories,

            created=entry_model.created,
            edited=entry_model.modified
        )
        return entry


class EntryPair(BaseModel):
    english: Optional[Entry]
    slovene: Optional[Entry]

    @staticmethod
    def from_model(pair_model: models.EntryPair):
        entry1 = None
        entry2 = None

        if pair_model.entry1:
            entry1 = Entry.from_model(pair_model.entry1)
        if pair_model.entry2:
            entry2 = Entry.from_model(pair_model.entry2)

        pair = EntryPair(
            english=entry1,
            slovene=entry2
        )
        return pair

    @staticmethod
    def from_list_models(model_list: List[models.EntryPair]):
        schema_list = []
        for item in model_list:
            schema_list.append(EntryPair.from_model(item))
        return schema_list
