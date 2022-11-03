from fastapi import APIRouter, HTTPException, status

from app.crud import controller_data as controller_data_crud
from app.schemas import controller_data as controller_data_schemas

router = APIRouter()


@router.post('/create_controller_data')
async def create_controller_data(controller_data: controller_data_schemas.ControllerDataCreate):
    if not await controller_data_crud.create_controller_data(data=controller_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/get_controller_data', response_model=list[controller_data_schemas.ControllerData] | list)
async def get_controller_data(controller_id: int, limit: int = 10):
    return await controller_data_crud.get_controller_data(controller_id=controller_id, limit=limit)


@router.get('/get_last_controller_data', response_model=controller_data_schemas.ControllerData | list)
async def get_controller_data(controller_id: int):
    return await controller_data_crud.get_last_controller_data(controller_id=controller_id)
