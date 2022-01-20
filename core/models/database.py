import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import asyncpg


# TODO: Change this in deployment
user = "kolomon"
password = "kolomon"
server = "localhost:5432"
db_name = "kolomon_db"
DATABASE_URL = f"postgresql://{user}:{password}@{server}/{db_name}"

# TODO: In production, add SSL = True!!!
database = databases.Database(DATABASE_URL)

# engine = create_engine(DATABASE_URL)

Base = declarative_base()


# Isn't used - would create/rewrite relations in DB (we use alembic for that)
# def init_db():
#     Base.metadata.create_all(bind=engine)


async def connect_db():
    await database.connect()


async def disconnect_db():
    await database.disconnect()
