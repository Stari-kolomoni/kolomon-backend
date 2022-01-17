from fastapi import Depends
from pydantic import BaseModel
from pydantic.main import Any

from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pagination import Paginator


# DATABASE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SECURITY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_request_form = OAuth2PasswordRequestForm


# PERMISSIONS
permissions = {
    'read_only': 1,
    'write': 2,
    'moderate': 3,
    'admin': 4
}


# PAGINATION
PAGE_DATA_SIZE = 50
paginator = Paginator(PAGE_DATA_SIZE)


# SWAGGER OPTIONS
swagger_parameters = {
    "syntaxHighlight.theme": "agate"
}


# API MESSAGE SCHEME
class Message(BaseModel):
    message: str


# Custom error exception class
class GeneralBackendException(Exception):
    def __init__(self, code: int = 500, message: str = ""):
        self.message = message
        self.code = code
