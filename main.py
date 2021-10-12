from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from users import models, users, auth
from lexicon import lexicon
from database import engine
from dependencies import oauth2_scheme, oauth2_request_form, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS rules to allow using the API on the frontend
allowed_cors_origins = [
    "http://localhost:8080",
    # TODO Add production URL and other things that need to be whitelisted, possibly through a configuration file
    #   Maybe we could even do "*"?
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(lexicon.router)


@app.get('/ping')
async def ping():
    return {"message": "pong"}


@app.get('/check')
async def check(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authorized."}


@app.post('/token', response_model=auth.Token)
def login(form_data: oauth2_request_form = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }