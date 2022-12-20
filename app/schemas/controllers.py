from datetime import datetime
from pydantic import BaseModel


class ControllersBase(BaseModel):
    controller_address: str | None
    local_address: str | None


class ControllerCreate(ControllersBase):
    login: str
    password: str


class ControllerUpdate(ControllerCreate):
    id: int


class Controllers(ControllersBase):
    id: int

    class Config:
        orm_mode = True


class ControllersWithControllerData(Controllers):
    status: bool | None
    charge: int | None
    create_data_datetime: datetime | None


class CountControllers(BaseModel):
    count: int
