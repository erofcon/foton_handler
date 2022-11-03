from datetime import datetime

from asyncpg.exceptions import IntegrityConstraintViolationError
from app.models.database import database
from app.models import controller_data as controller_data_model
from app.schemas import controller_data as controller_data_schemas


async def get_controller_data(controller_id: int, limit: int = 10) -> controller_data_schemas.ControllerData:
    query = controller_data_model.controller_data.select().where(
        controller_data_model.controller_data.c.controller_id == controller_id
    ).limit(limit=limit)

    return await database.fetch_all(query=query)


async def get_last_controller_data(controller_id: int) -> controller_data_schemas.ControllerData:
    query = controller_data_model.controller_data.select().where(
        controller_data_model.controller_data.c.controller_id == controller_id).order_by(
        controller_data_model.controller_data.c.id.desc())

    return await database.fetch_one(query=query)


async def create_controller_data(data: controller_data_schemas.ControllerDataCreate) -> bool:
    query = controller_data_model.controller_data.insert().values(
        vout=data.vout,
        temp=data.temp,
        charge=data.charge,
        relay=data.relay,
        vch=data.vch,
        data_datetime=datetime.utcnow(),
        controller_id=data.controller_id
    )

    try:
        return await database.execute(query=query)
    except IntegrityConstraintViolationError:
        return False
