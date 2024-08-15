import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationMixinSchema(BaseModel):
    full_amount: PositiveInt
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime.datetime = datetime.datetime.now()
    close_date: Optional[datetime.datetime] = None
