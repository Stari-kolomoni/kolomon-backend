from fastapi import Depends

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
