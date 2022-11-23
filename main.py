from fastapi import FastAPI

from app.log import log
from app.models.database import database
from app.routers.background_task import router as background_task_router
from app.routers.controllers import router as controllers_router
from app.routers.controller_data import router as controller_data_router
from app.routers.users import router as users_router
from app.routers.token import router as token_router
from app.async_background_task.foton_task import schedular

local_log = log.get_logger(__name__)

app = FastAPI()

app.include_router(router=background_task_router)
app.include_router(router=controllers_router)
app.include_router(router=controller_data_router)
app.include_router(router=users_router)
app.include_router(router=token_router)


@app.on_event('startup')
async def startup():
    await database.connect()
    schedular.foton_task_start()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
