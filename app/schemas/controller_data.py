from datetime import datetime
from pydantic import BaseModel


class ControllerDataBase(BaseModel):
    vin: int
    vout: int
    temp: int
    charge: int
    relay: int
    year: int
    month: int
    date: int
    hour: int
    min: int
    sec: int
    status: bool
    data_datetime: datetime
    controller_id: int


class ControllerDataCreate(ControllerDataBase):
    pass


class ControllerData(ControllerDataBase):
    id: int

    class Config:
        orm_mode = True
