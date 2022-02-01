from typing import Optional

from sqlalchemy import update, func, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from starlette.datastructures import QueryParams

import core.models.dal_dependencies as dd
import core.models.users_model as um
import core.schemas.users_schema as us


class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_users(self, params) -> tuple[list[us.User], int]:
        count_stm = func.count(um.User.id)
        count_query = await self.db_session.execute(count_stm)
        count: int = count_query.scalar()

        content_stm = select(um.User.id, um.User.username, um.User.display_name, um.User.is_active)
        content_stm = dd.paging_filter_sort(content_stm, params)
        content_query = await self.db_session.execute(content_stm)
        content = content_query.all()

        return content, count

    async def get_user(self, user_id: int) -> Optional[us.UserDetail]:
        query = await self.db_session.get(um.User, user_id)
        if query:
            return us.UserDetail.from_model(query)
        else:
            return None

    async def get_user_by_username(self, username: str) -> Optional[us.UserDetail]:
        statement = select(um.User).where(um.User.username == username)
        query = await self.db_session.execute(statement)
        result: um.User = query.scalars().first()

        if result:
            return us.UserDetail.from_model(result)
        else:
            return None

    async def get_user_credentials_by_username(self, username: str) -> Optional[us.UserLogin]:
        statement = select(um.User.id, um.User.username, um.User.hashed_passcode).where(um.User.username == username)
        query = await self.db_session.execute(statement)
        result: um.User = query.first()

        if result:
            return us.UserLogin.from_model(result)
        else:
            return None

    async def delete_user(self, user_id: int) -> bool:
        try:
            # Because SQLAlchemy many-to-many relationship cascading just doesn't work
            query = delete(um.RoleToUser).where(um.RoleToUser.user_id == user_id)
            query.execution_options(synchronize_session='fetch')
            await self.db_session.execute(query)

            query = delete(um.User).where(um.User.id == user_id)
            query.execution_options(synchronize_session='fetch')
            deleted = await self.db_session.execute(query)

            if deleted.rowcount == 0:
                await self.db_session.rollback()
                return False

            self.db_session.flush()
            return True
        except:
            await self.db_session.rollback()

    async def create_user(self, user: us.UserCreate) -> Optional[us.UserDetail]:
        db_user = um.User.from_schema(user)
        self.db_session.add(db_user)

        try:
            await self.db_session.flush()
            await self.db_session.refresh(db_user)
            return db_user
        except:
            await self.db_session.rollback()
            return None

    async def update_user(self, user_data: us.UserUpdate, user_id: int) -> (bool, str):
        query = update(um.User).where(um.User.id == user_id)
        if user_data.display_name:
            query = query.values(display_name=user_data.display_name)
        if user_data.password:
            query = query.values(hashed_passcode=user_data.password)
        query.execution_options(synchronize_session='fetch')

        try:
            changed: CursorResult = await self.db_session.execute(query)
            if changed.rowcount == 0:
                return False, "User not found"
            return True, "User updated"
        except:
            await self.db_session.rollback()
            return False, "Database error"

    async def get_user_roles(self, user_id: int, params: Optional[QueryParams]) -> (list[us.Role], int):
        # I hate this - it's slow
        roles_count: int = -1
        if params:
            count_stm = \
                select(func.count()).select_from(select(um.Role).filter(um.Role.users.any(id=user_id)).subquery())
            count_query = await self.db_session.execute(count_stm)
            roles_count = count_query.scalar()

        statement_filter_by_id = \
            select(um.Role.id, um.Role.name, um.Role.permissions).filter(um.Role.users.any(id=user_id))
        statement_paged_sort = dd.paging_filter_sort(statement_filter_by_id, params)

        content_query = await self.db_session.execute(statement_paged_sort)
        result = content_query.all()

        return result, roles_count

    async def get_user_roles_by_username(self, username: str) -> list[us.Role]:
        stm = select(um.Role.id, um.Role.name, um.Role.permissions) \
            .filter(um.Role.users.any(username=username))
        query = await self.db_session.execute(stm)

        result = query.all()
        return result

    async def create_user_roles(self, user_id: int, role_ids: list[int]) -> (bool, str):
        user_stm = select(um.User) \
            .where(um.User.id == user_id) \
            .options(selectinload(um.User.roles))
        user_query = await self.db_session.execute(user_stm)

        user = user_query.scalar()
        if not user:
            return False, "User not found"

        for role_id in role_ids:
            role = await self.db_session.get(um.Role, role_id)
            if role:
                user.roles.append(role)

        try:
            await self.db_session.flush()
            return True, "Roles appended"
        except:
            await self.db_session.rollback()
            return False, "Database error"

    async def remove_user_roles(self, user_id: int, role_ids: list[int]) -> (bool, str):
        user_stm = select(um.User).where(um.User.id == user_id).options(selectinload(um.User.roles))
        user_query = await self.db_session.execute(user_stm)

        user = user_query.scalar()
        if not user:
            return False, "User not found"

        for role_id in role_ids:
            role = await self.db_session.get(um.Role, role_id)
            if role:
                try:
                    user.roles.remove(role)
                except:
                    print("Role not in list")

        try:
            await self.db_session.flush()
            return True, "Roles removed"
        except:
            await self.db_session.rollback()
            return False, "Database error"
