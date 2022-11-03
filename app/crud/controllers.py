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


async def get_all_controllers() -> list[controllers_schemas.Controllers]:
    query = controllers_model.controllers.select()

    return await database.fetch_all(query=query)
