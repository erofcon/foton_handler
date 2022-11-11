from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import controllers as controllers_crud
from app.crud import users as users_crud
from app.schemas import controllers as controllers_schemas
from app.schemas import users as users_schemas

router = APIRouter()


@router.post('/create_controller')
async def create_controller(controller: controllers_schemas.ControllerCreate):
    if not await controllers_crud.create_controller(controller=controller):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/get_controllers', response_model=list[controllers_schemas.ControllersWithControllerData] | None)
async def get_controllers(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await controllers_crud.get_all_controllers_custom()
