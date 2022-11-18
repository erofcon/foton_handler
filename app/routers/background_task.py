from fastapi import Depends, APIRouter, HTTPException, status
from apscheduler.schedulers.base import STATE_PAUSED, STATE_RUNNING

from app.async_background_task.foton_task import schedular
from app.crud import users as users_crud
from app.schemas import users as users_schemas
from app.schemas import background_task as background_task_schemas

router = APIRouter()


@router.post('/task_pause')
async def task_pause(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    if schedular.task_check_status() == STATE_RUNNING:
        schedular.foton_task_pause()

    return HTTPException(status_code=status.HTTP_200_OK, detail='task is paused')


@router.post('/task_resume')
async def task_resume(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    if not current_user.is_super_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    if schedular.task_check_status() == STATE_PAUSED:
        schedular.foton_task_resume()

    return HTTPException(status_code=status.HTTP_200_OK, detail='task resumed')


@router.get('/check_task_status', response_model=background_task_schemas.TaskStatus)
async def check_task_status(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    task_status = schedular.task_check_status()
    status_detail = background_task_schemas.TaskStatus(task_status=0)

    if task_status == STATE_RUNNING:
        status_detail.task_status = 1
    elif task_status == STATE_PAUSED:
        status_detail.task_status = 2

    return status_detail
