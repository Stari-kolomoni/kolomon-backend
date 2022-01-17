from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from users import models, users, auth
from lexicon import lexicon
from database import engine
from dependencies import oauth2_scheme, oauth2_request_form, get_db, swagger_parameters, Message,\
    GeneralBackendException

models.Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters=swagger_parameters)


# Add custom exception for general error handling
@app.exception_handler(GeneralBackendException)
async def not_found_exception_handler(request: Request, exc: GeneralBackendException):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message}
    )


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


@app.get('/ping', response_model=Message, summary="Used to test server responsiveness")
async def ping():
    msg = Message(message="Pong")
    return msg


@app.get('/check', response_model=Message, summary="Used to test authorization")
async def check(token: str = Depends(oauth2_scheme)):
    msg = Message(message="You are authorized")
    return msg


@app.post('/token', response_model=auth.Token, summary="Authorisation token retrieval")
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


# Defining OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stari kolomoni",
        version="1.0",
        description="Fantazijska podatkovna baza",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
