import datetime

from pydantic import BaseModel


class MachineResponse(BaseModel):
    status_smoke: bool


class RegisterDevice(BaseModel):
    vk_login: str
    vk_password: str


class UserSchema(BaseModel):
    id: int
    vk_login: str
    vk_password: str

    class Config:
        orm_mode = True


class StatisticSchema(BaseModel):
    id: int
    user_id: int
    time_stamp: datetime.datetime
    mio_value: int

    class Config:
        orm_mode = True
