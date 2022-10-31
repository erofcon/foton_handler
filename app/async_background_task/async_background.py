import os
from datetime import datetime

import asyncio
from httpx import AsyncClient, HTTPError
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def get_pokemon(session: AsyncClient, url: str, i: int):
    try:
        response = await session.get(url=url)
        response.raise_for_status()

        if response.status_code == 200:
            pokemon = response.json()
            print(pokemon['name'], ' ', i)

    except HTTPError as exc:
        print(f"Error while requesting {exc.request.url!r}.")


async def background_task():
    print("____ new _____")
    async with AsyncClient() as client:
        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(get_pokemon(session=client, url=url, i=number)))

        await asyncio.gather(*tasks)


def tick():
    print(f'This time is: {datetime.now()}')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(background_task, trigger='interval', seconds=3)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
