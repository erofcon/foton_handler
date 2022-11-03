from pydantic import BaseModel


class UsersBase(BaseModel):
    username: str
    is_super_user: bool


class CreateUsers(UsersBase):
    password: str


class Users(UsersBase):
    id: int

    class Config:
        orm_mode = True
