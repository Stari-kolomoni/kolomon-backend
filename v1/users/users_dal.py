from typing import Optional, List

from sqlalchemy import update, func, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload

import core.models.dal_dependencies as dd
import core.models.users_model as um
import core.schemas.users_schema as us


class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_users(self, params) -> (List[us.User], int):
        count_stm = func.count(um.User.id)
        count_query = await self.db_session.execute(count_stm)
        count: int = count_query.scalar()

        content_stm = select(um.User.id, um.User.username, um.User.display_name, um.User.is_active)
        content_stm = dd.paging_filter_sort(content_stm, params)
        content_query = await self.db_session.execute(content_stm)
        content = content_query.all()
        return content, count

    async def get_user(self, user_id: int) -> us.UserDetail:
        user = None
        query = await self.db_session.get(um.User, user_id)
        if query:
            user = us.UserDetail.from_model(query)
        return user

    async def get_user_by_username(self, username: str) -> us.UserDetail:
        user = None
        stm = select(um.User).where(um.User.username == username)
        query = await self.db_session.execute(stm)
        res: um.User = query.scalars().first()
        if res:
            user = us.UserDetail.from_model(res)
        return user

    async def get_user_credentials_by_username(self, username: str) -> us.UserLogin:
        user = None
        stm = select(um.User.id, um.User.username, um.User.hashed_passcode)\
            .where(um.User.username == username)
        query = await self.db_session.execute(stm)
        res: um.User = query.first()
        if res:
            user = us.UserLogin.from_model(res)
        return user

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

    async def get_user_roles(self, user_id: int, params) -> (List[us.Role], int):
        # I hate this - it's slow
        count = -1
        if params:
            count_stm = select(func.count()).select_from(select(um.Role).filter(um.Role.users.any(id=user_id)).subquery())
            count_query = await self.db_session.execute(count_stm)
            count: int = count_query.scalar()

        stm = select(um.Role.id, um.Role.name, um.Role.permissions).filter(um.Role.users.any(id=user_id))
        stm = dd.paging_filter_sort(stm, params)
        content_query = await self.db_session.execute(stm)
        result = content_query.all()
        return result, count

    async def get_user_roles_by_username(self, username: str) -> List[us.Role]:
        stm = select(um.Role.id, um.Role.name, um.Role.permissions).filter(um.Role.users.any(username=username))
        query = await self.db_session.execute(stm)
        result = query.all()
        return result

    async def create_user_roles(self, user_id: int, role_ids: List[int]) -> (bool, str):
        user_stm = select(um.User).where(um.User.id == user_id).options(selectinload(um.User.roles))
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

    async def remove_user_roles(self, user_id: int, role_ids: List[int]) -> (bool, str):
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
