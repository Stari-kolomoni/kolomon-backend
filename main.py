from logging.config import dictConfig

from fastapi import FastAPI

from core.models.database import connect_db, disconnect_db
from core.logging import init_logger

init_logger()

app = FastAPI()


@app.on_event('startup')
async def startup():
    await connect_db()


@app.on_event('shutdown')
async def shutdown():
    await disconnect_db()
