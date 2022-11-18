from datetime import datetime

from fastapi import APIRouter, Depends

from app.crud import controller_data as controller_data_crud
from app.crud import users as users_crud
from app.schemas import users as users_schemas

router = APIRouter()


@router.get('/get_controller_data')
async def get_controller_data(controller_id: int, start_datetime: datetime, end_datetime: datetime,
                              current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await controller_data_crud.get_controller_data_between_two_datetime(controller_id=controller_id,
                                                                               start_datetime=start_datetime,
                                                                               end_datetime=end_datetime)
