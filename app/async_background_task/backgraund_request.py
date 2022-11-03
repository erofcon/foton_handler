from datetime import datetime
import asyncio

from httpx import AsyncClient, HTTPError

from app.models.database import database
from app.models import controller_data as controller_data_model
from app.crud import controllers as controllers_crud


async def get_controller_data(session: AsyncClient, url: str, controller_id: int):
    try:
        response = await session.get(url=url)
        response.raise_for_status()

        if response.status_code == 200:
            controller_data = response.json()

            query = controller_data_model.controller_data.insert().values(
                vout=12,
                temp=30,
                charge=12,
                relay=42,
                vch=64,
                data_datetime=datetime.utcnow(),
                controller_id=controller_id
            )

            await database.execute(query=query)

            print(controller_data['name'], ' ', controller_id)

    except HTTPError as exc:
        print(f"Error while requesting {exc.request.url!r}.")


async def foton_request_task():
    print("____ new _____")
    async with AsyncClient() as client:
        controllers = await controllers_crud.get_all_controllers()
        tasks = []
        for i in range(len(controllers)):
            url = f'https://pokeapi.co/api/v2/pokemon/{controllers[i].id}'
            tasks.append(
                asyncio.ensure_future(get_controller_data(session=client, url=url, controller_id=controllers[i].id)))

        await asyncio.gather(*tasks)
