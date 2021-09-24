from fastapi import Depends

from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


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
