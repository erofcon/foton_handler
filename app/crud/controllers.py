from sqlalchemy import text
from asyncpg.exceptions import IntegrityConstraintViolationError

from app.models.database import database
from app.models import controllers as controllers_model
from app.schemas import controllers as controllers_schemas


async def create_controller(controller: controllers_schemas.ControllerCreate) -> bool:
    query = controllers_model.controllers.insert().values(
        controller_address=controller.controller_address,
        login=controller.login,
        password=controller.password
    )
    try:
        return await database.execute(query=query)
    except IntegrityConstraintViolationError:
        return False


async def get_all_controllers():
    query = controllers_model.controllers.select()

    return await database.fetch_all(query=query)


async def get_all_controllers_custom():
    query = text("""SELECT  c.id, c.controller_address, cd.status
                    FROM    controllers c LEFT JOIN
                    (
                        SELECT  controller_id,
                        MAX(create_data_datetime) MaxDate
                        FROM  controller_data
                        GROUP BY controller_id
                    ) MaxDates ON c.id = MaxDates.controller_id LEFT JOIN
                    controller_data cd ON MaxDates.controller_id = cd.controller_id
                    AND MaxDates.MaxDate = cd.create_data_datetime""")

    return await database.fetch_all(query=query)
