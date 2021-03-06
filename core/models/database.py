from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from ..configuration import config

DATABASE_URL = f"postgresql+asyncpg://" \
               f"{config.DATABASE.USER}:{config.DATABASE.PASSWORD}" \
               f"@{config.DATABASE.HOST}/{config.DATABASE.DATABASE_NAME}"

# TODO: Add SSL = True in deployment!
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def connect_db():
    return await engine.begin()


async def disconnect_db():
    await engine.dispose()


async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session
