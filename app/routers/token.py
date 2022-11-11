from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import users as users_crud
from app.crud import token as token_crud
from app.schemas import token as token_schemas

router = APIRouter()


@router.post('/token', response_model=token_schemas.Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_crud.authenticate_user(username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    return token_crud.create_access_token(data={'sub': user.username, 'is_super_user': user.is_super_user})


@router.post('/refresh', response_model=token_schemas.Token)
async def refresh_token(token: str, username: str):
    return token_crud.create_refresh_token(token=token, username=username)
