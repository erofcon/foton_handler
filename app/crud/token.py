from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt

from app.schemas import token as token_schemas
from app.schemas.token import Token

SECRET_KEY = "09d25e094fa4nr6a355tu8z816vb7ax5312af7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 3


def create_access_token(
        data: dict,
        access_token_expire_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token_expire_minute: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
) -> token_schemas.Token:
    access_encode = data.copy()
    refresh_encode = data.copy()

    if access_token_expire_delta:
        access_expire = datetime.utcnow() + access_token_expire_delta
    else:
        access_expire = datetime.utcnow() + timedelta(minutes=15)

    if refresh_token_expire_minute:
        refresh_expire = datetime.utcnow() + refresh_token_expire_minute
    else:
        refresh_expire = datetime.utcnow() + timedelta(days=2)

    access_encode.update({'exp': access_expire})
    access_encoded_jwt = jwt.encode(access_encode, SECRET_KEY, algorithm=ALGORITHM)

    refresh_encode.update({'exp': refresh_expire})
    refresh_encoded_jwt = jwt.encode(refresh_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token_schemas.Token(access_token=access_encoded_jwt, refresh_token=refresh_encoded_jwt, token_type='bearer',
                               username=data.get('sub'),
                               is_super_user=data.get('is_super_user'))


def create_refresh_token(token: str, username: str) -> Token | HTTPException:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY)

        if datetime.utcfromtimestamp(payload.get('exp')) > datetime.now() and username == payload.get('sub'):
            return create_access_token(data={'sub': username, 'is_super_user': payload.get('is_super_user')})

        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )
