from typing import Optional, List

from sqlalchemy import update, func, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import core.models.users_model as um
import core.schemas.users_schema as us
import core.models.dal_dependencies as dd


class RoleDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_roles(self, params) -> (List[us.Role], int):
        count_stm = func.count(um.Role.id)
        count_query = await self.db_session.execute(count_stm)
        count: int = count_query.scalar()

        content_stm = select(um.Role.id, um.Role.name, um.Role.permissions)
        content_stm = dd.paging_filter_sort(content_stm, params)
        content_query = await self.db_session.execute(content_stm)
        content = content_query.all()

        return content, count

    async def get_role(self, role_id: int) -> Optional[us.Role]:
        query = await self.db_session.get(um.Role, role_id)
        if query:
            return us.Role.from_model(query)
        else:
            return None

    async def delete_role(self, role_id: int) -> bool:
        query = delete(um.Role).where(um.Role.id == role_id)
        query.execution_options(synchronize_session='fetch')

        deleted = await self.db_session.execute(query)
        return deleted.rowcount != 0

    async def create_role(self, role: us.RoleCreate) -> Optional[us.Role]:
        db_role = um.Role.from_schema(role)
        self.db_session.add(db_role)

        try:
            await self.db_session.flush()
            await self.db_session.refresh(db_role)
            return db_role
        except:
            await self.db_session.rollback()
            return None

    async def update_role(self, role_data: us.RoleUpdate, role_id: int) -> tuple[bool, str]:
        query = update(um.Role).where(um.Role.id == role_id)
        if role_data.name:
            query = query.values(name=role_data.name)
        elif role_data.permissions >= 0:
            query = query.values(permissions=role_data.permissions)
        query.execution_options(synchronize_session='fetch')

        try:
            changed: CursorResult = await self.db_session.execute(query)
            if changed.rowcount == 0:
                return False, "Role not found"
            return True, "Role updated"
        except:
            await self.db_session.rollback()
            return False, "Database error"
