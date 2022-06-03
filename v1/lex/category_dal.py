from sqlalchemy.orm import Session

import core.models.lex_model as models
import core.schemas.lex_schema as schemas


class CategoryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_category(self, category_create: schemas.CategoryCreate):
        category = category_create.to_category_instance()
        await category.save(self.db_session)

    async def remove_category(self, category_id: int):
        await models.Category.delete(category_id, self.db_session)

    async def update_category(self, category_id: int, category_update: schemas.CategoryCreate):
        category = category_update.to_category_instance()
        category.id = category_id
        await category.update(self.db_session)

    async def retrieve_categories(self, filters: dict):
        model, count = await models.Category.retrieve_all(filters, self.db_session)
        list_schema = schemas.Category.list_from_model(model)
        schema = schemas.CategoryList(
            categories=list_schema,
            full_count=count
        )
        return schema

    async def retrieve_entries_by_category(self, filters: dict, category_id: int):
        return await models.Entry.retrieve_by_category(filters, category_id, self.db_session)
