from pydantic import BaseModel


class ControllersBase(BaseModel):
    controller_address: str
    login: str
    password: str


class ControllerCreate(ControllersBase):
    pass


class Controllers(ControllersBase):
    id: int

    class Config:
        orm_mode = True
