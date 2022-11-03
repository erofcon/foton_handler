from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from asyncpg.exceptions import IntegrityConstraintViolationError

from app.models.database import database
from app.crud import token as token_crud
from app.models import users as users_model
from app.schemas import users as users_schemas
from app.schemas import token as token_schemas

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def _verify_password(plan_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plan_password, hash=hashed_password)


def _get_password_hash(password: str):
    return pwd_context.hash(secret=password)


async def _get_user_by_name(username: str) -> users_schemas.CreateUsers | None:
    query = users_model.users.select().where(users_model.users.c.username == username)
    return await database.fetch_one(query=query)


async def create_user(user: users_schemas.CreateUsers) -> bool:
    hash_password = _get_password_hash(user.password)

    query = users_model.users.insert().values(
        username=user.username,
        password=hash_password,
        is_super_user=user.is_super_user,
    )

    try:
        return await database.execute(query=query)
    except IntegrityConstraintViolationError:
        return False


async def get_current_user(token: str = Depends(oauth2_scheme)) -> users_schemas.UsersBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=token_crud.SECRET_KEY, algorithms=[token_crud.ALGORITHM])
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception

        token_data = token_schemas.TokenData(username=username)

    except jwt.JWTClaimsError:
        raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await _get_user_by_name(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_all_users(limit: int = 10) -> list[users_schemas.UsersBase] | list:
    query = users_model.users.select().limit(limit=limit)

    return await database.fetch_all(query=query)


async def authenticate_user(username: str, password: str) -> users_schemas.UsersBase | None:
    user = await _get_user_by_name(username=username)

    if not user:
        return None

    if not _verify_password(plan_password=password, hashed_password=user.password):
        return None

    return user
