from typing import List, Optional

from sqlalchemy import update, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import core.models.users_model as model
import core.schemas.users_schema as schema


class RoleDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_roles(self) -> List[schema.Role]:
        stm = select(model.Role)
        query = await self.db_session.execute(stm)
        return query.scalars().all()

    async def get_role(self, role_id: int) -> Optional[schema.Role]:
        stm = select(model.Role).where(model.Role.id == role_id)
        query = await self.db_session.execute(stm)
        return query.scalars().first()

    async def create_role(self, role: schema.RoleCreate) -> schema.Role:
        db_role = model.Role(
            name=role.name,
            permissions=role.permissions
        )
        self.db_session.add(db_role)
        await self.db_session.flush()
        await self.db_session.refresh(db_role)
        return db_role

    async def update_role(self, role_data: schema.RoleUpdate, role_id: int) -> Optional[schema.Role]:
        role: Optional[schema.Role] = await self.get_role(role_id)
        if not role:
            return None

        query = update(model.Role).where(model.Role.id == role_id)
        if role_data.name:
            query = query.values(name=role_data.name)
            role.name = role_data.name
        if role_data.permissions:
            query = query.values(permissions=role_data.permissions)
            role.permissions = role_data.permissions
        query.execution_options(synchronize_session='fetch')
        changed: CursorResult = await self.db_session.execute(query)

        if changed.rowcount == 0:
            return None
        return role

    async def delete_role(self, role_id: int) -> bool:
        query = delete(model.Role).where(model.Role.id == role_id)
        query.execution_options(synchronize_session='fetch')
        deleted: CursorResult = await self.db_session.execute(query)

        if deleted.rowcount == 0:
            return False
        return True
