from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import GeneralBackendException
from core.message_types import Message
from core.models.database import connect_db, disconnect_db
from core.logging import init_logger, logger

from v1.api import router as v1_router

init_logger()

app = FastAPI()


@app.exception_handler(GeneralBackendException)
async def not_found_exception_handler(request: Request, exc: GeneralBackendException):
    msg = Message(detail=exc.message)
    return JSONResponse(
        status_code=exc.code,
        content=msg.dict()
    )


@app.on_event('startup')
async def startup():
    logger.info("Starting up...")
    await connect_db()
    logger.info("Database connected!")


@app.on_event('shutdown')
async def shutdown():
    await disconnect_db()
    logger.info("Database disconnected!")


app.include_router(v1_router)
