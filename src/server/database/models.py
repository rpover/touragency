from pydantic import BaseModel
from typing import Optional


class BaseModelModify(BaseModel):
    id: Optional[int] = 1


class Ticket(BaseModelModify):
    tour_id: int
    date_start: str
    date_end: str
    user_id: int


class User(BaseModelModify):
    name: str
    surname: str
    phone: str
    password: Optional[str]
    power_level: int = 1


class Tour(BaseModelModify):
    country_id: int
    hours: int
    price: float


class Country(BaseModelModify):
    name: str


class UserAuth(BaseModel):
    phone: str
    password: str

