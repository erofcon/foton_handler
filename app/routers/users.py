from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import users as users_crud
from app.schemas import users as users_schemas

router = APIRouter()


@router.post('/create_user')
async def create_user(user: users_schemas.CreateUsers,
                      current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    if await users_crud.get_user_by_name(user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User exists')

    if not await users_crud.create_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/get_all_users', response_model=list[users_schemas.Users] | list)
async def get_all_users(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    return await users_crud.get_all_users(current_user=current_user.username)


@router.delete('/delete_user')
async def delete_controller(user_id: int,
                            current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    if await users_crud.delete_user(user_id=user_id):
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
