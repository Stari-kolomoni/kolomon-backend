import logging
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration for the server.
    Shamelessly copied from https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api"""

    LOGGER_NAME: str = "KolomoniBackend"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': "uvicorn.logging.DefaultFormatter",
            'fmt': LOG_FORMAT,
            'datefmt': "%d.%m.%Y, %H:%M:%S",
        },
    }
    handlers = {
        'default': {
            'formatter': "default",
            'class': "logging.StreamHandler",
            'stream': "ext://sys.stderr",
        }
    }
    loggers = {
        'KolomonBE_Logs': {'handlers': ['default'], 'level': LOG_LEVEL},
    }


def init_logger():
    dictConfig(LogConfig().dict())


logger = logging.getLogger(LogConfig.LOGGER_NAME)
