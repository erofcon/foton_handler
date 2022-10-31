from fastapi import FastAPI

from models.database import database
from routers.background_task import router as background_task_router
from async_background_task.foton_task import foton_task_start

app = FastAPI()

app.include_router(background_task_router)


@app.on_event('startup')
async def startup():
    await database.connect()
    foton_task_start()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
