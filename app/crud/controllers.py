from datetime import datetime

from sqlalchemy import text, update
from asyncpg.exceptions import IntegrityConstraintViolationError

from app.models.database import database
from app.models import controllers as controllers_model
from app.schemas import controllers as controllers_schemas


async def create_controller(controller: controllers_schemas.ControllerCreate) -> bool:
    query = controllers_model.controllers.insert().values(
        local_address=controller.local_address,
        controller_address=controller.controller_address,
        login=controller.login,
        password=controller.password,
        create_date_time=datetime.now(),
    )
    try:
        return await database.execute(query=query)
    except IntegrityConstraintViolationError:
        return False


async def get_controller_edit_data(controller_id: int) -> controllers_schemas.ControllerCreate:
    query = controllers_model.controllers.select().where(
        controllers_model.controllers.c.id == controller_id,
    )

    return await database.fetch_one(query=query)


async def get_all_controllers_custom():
    query = text("""
                SELECT c.id, c.controller_address, c.local_address, cd.status, chr.charge
                FROM controllers c
                LEFT JOIN
                ( 
                 SELECT  controller_id,
                 MAX(create_data_datetime) MaxDate
                 FROM  controller_data 
                 GROUP BY controller_id
                ) MaxDates 
                ON 
                c.id = MaxDates.controller_id 
                LEFT JOIN
                controller_data cd 
                ON MaxDates.controller_id = cd.controller_id AND MaxDates.MaxDate = cd.create_data_datetime
                left JOIN LATERAL 
                (
                 select charge, controller_id, create_data_datetime from controller_data 
                 WHERE charge>0 and controller_id=c.id
                 ORDER BY create_data_datetime desc limit 1
                ) chr on chr.controller_id=c.id
            """)

    return await database.fetch_all(query=query)


async def get_all_controllers() -> list[controllers_schemas.Controllers]:
    query = controllers_model.controllers.select()

    return await database.fetch_all(query=query)


async def get_controllers_count() -> int:
    query = text("""select count(id) from controllers""")

    return await database.fetch_one(query=query)


async def update_controller(controller: controllers_schemas.ControllerUpdate) -> bool:
    query = update(controllers_model.controllers).where(
        controllers_model.controllers.c.id == controller.id
    ).values(
        local_address=controller.local_address,
        controller_address=controller.controller_address,
        login=controller.login,
        password=controller.password,
        create_date_time=datetime.now(),
    )

    return await database.fetch_one(query=query)


async def delete_controller(controller_id: int) -> bool:
    try:
        query = text(f"""DELETE FROM controllers WHERE controllers.id = {controller_id}""")

        await database.execute(query=query)
        return True
    except Exception:
        return False
