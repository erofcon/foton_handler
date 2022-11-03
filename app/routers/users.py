from fastapi import APIRouter, HTTPException, status

from app.crud import users as users_crud
from app.schemas import users as users_schemas

router = APIRouter()


@router.post('/create_user')
async def create_user(user: users_schemas.CreateUsers):
    if not await users_crud.create_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/get_all_users', response_model=list[users_schemas.UsersBase] | list)
async def get_all_users(limit: int = 10):
    return await users_crud.get_all_users(limit=limit)
