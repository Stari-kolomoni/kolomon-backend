from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

from core.exceptions import GeneralBackendException
from core.message_types import Message
from core.models.database import connect_db, disconnect_db
from core.log import init_logger, logger

from v1.api import router as v1_router

init_logger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(GeneralBackendException)
async def not_found_exception_handler(_request: Request, exc: GeneralBackendException):
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


@app.get("/ping/")
async def check(_: Request):
    return Response(status_code=200)


app.include_router(v1_router)
