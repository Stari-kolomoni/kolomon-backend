import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# TODO: Change this in deployment
user = "admin"
password = ""
server = "localhost:5432"
db_name = "kolomonDB"
DATABASE_URL = f"postgresql://{user}:{password}@{server}/{db_name}"

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Isn't used - would create the models (we use alembic for that)
def init_db():
    Base.metadata.create_all(bind=engine)


async def connect_db():
    await database.connect()


async def disconnect_db():
    await database.disconnect()
