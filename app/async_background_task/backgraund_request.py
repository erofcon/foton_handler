import asyncio
from httpx import AsyncClient, HTTPError


async def get_pokemon(session: AsyncClient, url: str, i: int):
    try:
        response = await session.get(url=url)
        response.raise_for_status()

        if response.status_code == 200:
            pokemon = response.json()
            print(pokemon['name'], ' ', i)

    except HTTPError as exc:
        print(f"Error while requesting {exc.request.url!r}.")


async def foton_request_task():
    print("____ new _____")
    async with AsyncClient() as client:
        tasks = []
        for number in range(1, 151):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(get_pokemon(session=client, url=url, i=number)))

        await asyncio.gather(*tasks)
