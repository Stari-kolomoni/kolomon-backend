from sqlalchemy.orm import Session

import core.models.lex_model as models
import core.schemas.lex_schema as schemas


class TranslationStateDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_translation_state(self, state_create: schemas.TranslationStateCreate):
        state = state_create.to_state_instance()
        await state.save(self.db_session)

    async def remove_translation_state(self, state_id: int):
        await models.TranslationState.delete(state_id, self.db_session)

    async def retrieve_translation_state_by_id(self, state_id: int):
        state = await models.TranslationState.retrieve_by_id(state_id, self.db_session)
        return state

    async def retrieve_all_translation_states(self, filters):
        states, count = await models.TranslationState.retrieve_all(filters, self.db_session)
        schema_states = schemas.TranslationState.list_from_model(states)
        schema = schemas.TranslationStateList(
            translation_states=schema_states,
            full_count=count
        )
        return schema
