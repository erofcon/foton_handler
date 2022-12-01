from datetime import datetime
import asyncio

from httpx import AsyncClient, HTTPError, BasicAuth

from app.models.database import database
from app.models import controller_data as controller_data_model
from app.crud import controllers as controllers_crud


async def get_controller_data(session: AsyncClient, url: str, login: str, password: str, controller_id: int):
    for i in range(5):
        try:
            response = await session.get(url=url, auth=BasicAuth(username=login, password=password), timeout=10.0)
            response.raise_for_status()

            if response.status_code == 200:
                controller_data = response.json()

                query = controller_data_model.controller_data.insert().values(

                    vin=controller_data['vin'],
                    vout=controller_data['vout'],
                    temp=controller_data['temp'],
                    charge=controller_data['charge'],
                    relay=controller_data['relay'],
                    year=controller_data['year'],
                    month=controller_data['month'],
                    date=controller_data['date'],
                    hour=controller_data['hour'],
                    min=controller_data['min'],
                    sec=controller_data['sec'],
                    status=True,
                    create_data_datetime=datetime.now(),
                    controller_id=controller_id,
                )

                await database.execute(query=query)
                return

        except Exception:
            if i == 4:
                query = controller_data_model.controller_data.insert().values(

                    vin=0,
                    vout=0,
                    temp=0,
                    charge=0,
                    relay=0,
                    year=0,
                    month=0,
                    date=0,
                    hour=0,
                    min=0,
                    sec=0,
                    status=False,
                    create_data_datetime=datetime.now(),
                    controller_id=controller_id,
                )
                await database.execute(query=query)


async def foton_request_task():
    client = AsyncClient()
    tasks = []
    controllers = await controllers_crud.get_all_controllers()

    for i in range(len(controllers)):
        url = f'http://{controllers[i].controller_address}/data.json'
        tasks.append(
            asyncio.ensure_future(get_controller_data(session=client, url=url,
                                                      login=controllers[i].login, password=controllers[i].password,
                                                      controller_id=controllers[i].id)))

    await asyncio.gather(*tasks)
    await client.aclose()

    # async with AsyncClient() as client:
    #     controllers = await controllers_crud.get_all_controllers()
    #     tasks = []
    #     for i in range(len(controllers)):
    #         url = f'http://{controllers[i].controller_address}/data.json'
    #         tasks.append(
    #             asyncio.ensure_future(get_controller_data(session=client, url=url,
    #                                                       login=controllers[i].login, password=controllers[i].password,
    #                                                       controller_id=controllers[i].id)))
    #
    #     await asyncio.gather(*tasks)
