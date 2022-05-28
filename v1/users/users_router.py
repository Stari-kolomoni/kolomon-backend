from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from starlette.datastructures import QueryParams
from starlette.responses import JSONResponse

from core.exceptions import GeneralBackendException
from core.message_types import Message
from core.models.database import async_session
from core.configuration import config
from core.schemas.users_schema import TokenData, User, UserDetail, UserCreate, UserUpdate, Role, UserLogin

import v1.doc_strings as doc_str
from v1.dependencies import oauth2_scheme
from v1.users.users_dal import UserDAL

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"])

####
# Utility functions
####
async def get_user_dal() -> UserDAL:
    """
    FastAPI injectable to provide access to users in the database.
    """
    async with async_session() as session:
        async with session.begin():
            return UserDAL(session)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the validity of the password by comparing it to a hash of the expected password.

    :param plain_password: Plain-text password (will be hashed and compared).
    :param hashed_password: Pasword hash to compare to.
    :return: Boolean indicating whether the password matched the hash.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, TypeError):
        return False


def hash_password(password: str) -> str:
    """
    Hash the provided password.

    :param password: Password to hash.
    :return: Hashed password.
    """
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, database: UserDAL) -> Optional[UserLogin]:
    """
    Attempt to authenticate the user.

    :param username: Username to authenticate with.
    :param password: Password to authenticase with.
    :param database: UserDAL instance to use as the data access layer.
    :return: UserLogin instance if sucessfully authenticated, None otherwise.
    """
    user: Optional[UserLogin] = await database.get_user_credentials_by_username(username)
    is_valid_password: bool = verify_password(password, user.password)

    if user is None or is_valid_password is False:
        return None

    return user


async def get_current_user(
        database: UserDAL = Depends(get_user_dal),
        token: str = Depends(oauth2_scheme)
) -> UserDetail:
    """
    FastAPI injectable to fetch information about the authenticated user (via Bearer token).

    :param database: Instance of UserDAL to access users.
    :param token: Token from the Authentication header.
    :return: UserDetail instance of the logged-in user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload: dict = jwt.decode(token=token, key=config.JWT.SECRET_KEY, algorithms=[config.JWT.ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError as error:
        raise credentials_exception from error

    user = await database.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return user


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Create an access token for the user.

    :param data: Data to encode in the JWT.
    :param expires_delta: Timedelta of token expiration.
    :return: Access token.
    """
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT.SECRET_KEY, algorithm=config.JWT.ALGORITHM)

    return encoded_jwt


####
# Routes
####
@router.get("/",
            response_model=list[User],
            status_code=200,
            description=doc_str.GET_USERS)
async def read_users(
        req: Request,
        database: UserDAL = Depends(get_user_dal)
):
    """
    Get a list of registered users.
    Can be paginated using the skip and limit query parameters.
    """
    content, count = await database.get_users(req.query_params)

    json_content = jsonable_encoder(content)
    headers = {
        "X-Total-Count": str(count)
    }

    return JSONResponse(
        content=json_content, headers=headers
    )


@router.post("/",
             response_model=UserDetail,
             status_code=201,
             responses={400: {}},
             description=doc_str.POST_USER)
async def create_user(
        new_user: UserCreate,
        database: UserDAL = Depends(get_user_dal)
):
    """
    Create a new user.
    """
    new_user.password = hash_password(new_user.password)

    new_user = await database.create_user(new_user)
    if new_user is None:
        raise GeneralBackendException(400, "Username already taken")

    return new_user


@router.get("/me",
            response_model=UserDetail)
async def read_user_me(
        current_user: User = Depends(get_current_user)
):
    """
    Return information about the currently authenticated user (based on the Authorization header).
    """
    return current_user


@router.get("/me/perms")
async def read_user_me_permissions(
        current_user: User = Depends(get_current_user),
        database: UserDAL = Depends(get_user_dal)
):
    """
    Return information about the currently authenticated user's permissions (roles) (based on the Authorization header).
    """
    roles, _ = await database.get_user_roles(current_user.id, None)
    perms = 0
    for role in roles:
        perms = perms | role.permissions

    return {
        "permissions": perms
    }


@router.post("/token",
             description=doc_str.LOGIN)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        database: UserDAL = Depends(get_user_dal)
):
    """
    Perform a user log, generating a JWT token for further access.
    """
    user = await authenticate_user(form_data.username, form_data.password, database)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.JWT.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/{user_id}",
            response_model=UserDetail,
            status_code=200,
            responses={404: {}},
            description=doc_str.GET_USER)
async def read_user_details(
        user_id: int,
        database: UserDAL = Depends(get_user_dal)
):
    """
    Return information about a user by ID.
    """
    user = await database.get_user(user_id)
    if not user:
        raise GeneralBackendException(404, "User not found")

    return user


@router.put("/{user_id}",
            response_model=Message,
            status_code=200,
            responses={404: {}, 400: {}},
            description=doc_str.PUT_USER)
async def update_user(
        user_data: UserUpdate,
        user_id: int,
        database: UserDAL = Depends(get_user_dal),
        current_user: UserDetail = Depends(get_current_user)
):
    """
    Update user's information by ID. Only owners are allowed to update the account.
    """
    # TODO: Admin permission
    if user_id != current_user.id:
        raise GeneralBackendException(401, "You are not the owner of this account.")

    updated, msg = await database.update_user(user_data, user_id)
    if not updated:
        raise GeneralBackendException(404, msg)

    return Message(detail=msg)


@router.delete("/{user_id}", status_code=200,
               responses={404: {}}, description=doc_str.DELETE_USER)
async def remove_user(
        user_id: int,
        database: UserDAL = Depends(get_user_dal)
):
    """
    Delete a registered user.
    """
    deleted = await database.delete_user(user_id)
    if not deleted:
        raise GeneralBackendException(404, "User not found")

    return Message(detail="User deleted")


@router.get("/{user_id}/roles", response_model=list[Role], status_code=200,
            description=doc_str.GET_USER_ROLES)
async def read_user_roles(
        req: Request,
        user_id: int,
        database: UserDAL = Depends(get_user_dal)
):
    """
    Return a list of user roles.
    """
    content, count = await database.get_user_roles(user_id, req.query_params)

    json_content = jsonable_encoder(content)
    headers = {
        "X-Total-Count": str(count)
    }

    return JSONResponse(
        content=json_content, headers=headers
    )


@router.post("/{user_id}/roles", response_model=Message, status_code=200,
             description=doc_str.POST_USER_ROLES)
async def add_user_roles(
        user_id: int,
        role_ids: list[int],
        database: UserDAL = Depends(get_user_dal)
):
    """
    Add roles to user's permissions.
    """
    added, msg = await database.create_user_roles(user_id, role_ids)
    if not added:
        raise GeneralBackendException(404, msg)
    return Message(detail=msg)


@router.delete("/{user_id}/roles", response_model=Message, status_code=200,
               description=doc_str.DELETE_USER_ROLES)
async def remove_user_roles(
        user_id: int,
        role_ids: list[int],
        database: UserDAL = Depends(get_user_dal)
):
    """
    Remove roles from a user's permissions list.
    """
    removed, msg = await database.remove_user_roles(user_id, role_ids)
    if not removed:
        raise GeneralBackendException(404, msg)
    return Message(detail=msg)
