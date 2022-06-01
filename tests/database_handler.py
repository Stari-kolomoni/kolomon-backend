from core.models.database import async_session
import pytest_asyncio
from sqlalchemy import text


@pytest_asyncio.fixture
async def db():
    session = async_session()
    await session.begin()

    yield session

    sql = text("DELETE FROM entries")
    await session.execute(sql)
    await session.commit()
    await session.flush()

    await session.close()
