from datetime import datetime
from pydantic import BaseModel


class ControllerDataBase(BaseModel):
    vout: int
    temp: int
    charge: int
    relay: int
    vch: int
    controller_id: int


class ControllerDataCreate(ControllerDataBase):
    pass


class ControllerData(ControllerDataBase):
    id: int
    data_datetime: datetime

    class Config:
        orm_mode = True
