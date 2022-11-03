from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import users as users_crud
from app.crud import token as token_crud
from app.schemas import token as token_schemas

router = APIRouter()


@router.post('/token', response_model=token_schemas.Token)
async def get_token(from_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_crud.authenticate_user(username=from_data.username, password=from_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    return token_crud.create_access_token(data={'sub': user.username})
