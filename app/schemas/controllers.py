from pydantic import BaseModel


class ControllersBase(BaseModel):
    controller_address: str


class ControllerCreate(ControllersBase):
    login: str
    password: str


class Controllers(ControllersBase):
    id: int

    class Config:
        orm_mode = True


class ControllersWithControllerData(Controllers):
    status: bool | None
    charge: int | None


class CountControllers(BaseModel):
    count: int
