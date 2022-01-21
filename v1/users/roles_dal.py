from typing import List, Optional

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

    async def update_role(self, role: schema.RoleUpdate) -> schema.Role:
        pass
