from sqlalchemy import delete, func
from sqlalchemy.engine import CursorResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class MainDAL:
    def __init__(self, db_session: Session, model):
        self.db_session = db_session
        self.model = model

    @staticmethod
    def paging_filter_sort(query, params):
        limit = params.get('limit')
        skip = params.get('skip')
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)

        return query

    async def get_all_objects(self, params):
        count_stm = func.count(self.model.id)
        count_query = await self.db_session.execute(count_stm)
        count: int = count_query.scalar()

        content_stm = select(self.model)
        content_stm = MainDAL.paging_filter_sort(content_stm, params)

        content_query = await self.db_session.execute(content_stm)
        content = content_query.scalars().all()

        return content, count

    async def get_object(self, attr: str, cond: int):
        stm = select(self.model).where(getattr(self.model, attr) == cond)
        query = await self.db_session.execute(stm)
        return query.scalars().first()

    async def delete_object(self, attr: str, cond: int) -> bool:
        query = delete(self.model).where(getattr(self.model, attr) == cond)
        query.execution_options(synchronize_session='fetch')
        deleted: CursorResult = await self.db_session.execute(query)

        if deleted.rowcount == 0:
            return False
        return True
