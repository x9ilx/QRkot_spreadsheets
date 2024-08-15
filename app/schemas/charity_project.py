from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.mixins import DonationMixinSchema


NAME_MIN_LENGHT = 1
NAME_MAX_LENGTH = 100


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGHT,
        max_length=NAME_MAX_LENGTH,
    )
    description: str
    full_amount: PositiveInt

    @validator('description')
    def not_empty_description(cls, value):
        if not value:
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectCreate(CharityProjectBase):
    ...


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LENGHT,
        max_length=NAME_MAX_LENGTH,
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(DonationMixinSchema, CharityProjectBase):
    id: int

    class Config:
        orm_mode = True
