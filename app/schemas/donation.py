import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt

from app.schemas.mixins import DonationMixinSchema


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    ...


class DonationDBForSuperuser(DonationMixinSchema, DonationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
