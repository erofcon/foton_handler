import asyncio

from app.models.database import database
from app.crud import users as users_crud
from app.schemas import users as user_schemas


async def create_super_user():
    await database.connect()

    name: str = input("user name: ")
    password: str = input("user password ")

    user = user_schemas.CreateUsers(username=name, password=password, is_super_user=True)

    if await users_crud.create_user(user):
        print("user successfully created")
    else:
        print("error creating user")

    await database.disconnect()

if __name__ == '__main__':
    asyncio.run(create_super_user())
