from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_type = "postgresql"
host = "localhost"
port = "5432"
user = "kolomon"
password = "kolomon"
database = "kolomondb"

SQLALCHEMY_DATABASE_URL = f"{db_type}://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
