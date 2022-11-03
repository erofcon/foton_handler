from fastapi import APIRouter, HTTPException, status

from app.crud import controllers as controllers_crud
from app.schemas import controllers as controllers_schemas

router = APIRouter()


@router.post('/create_controller')
async def create_controller(controller: controllers_schemas.ControllerCreate):
    if not await controllers_crud.create_controller(controller=controller):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/get_controllers', response_model=controllers_schemas.ControllersBase | list)
async def get_controllers():
    return await controllers_crud.get_all_controllers()
