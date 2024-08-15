from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDCDonation(CRUDBase[Donation, DonationCreate, None]):
    def __init__(self) -> None:
        super().__init__(Donation)

    async def get_user_donation(
        self,
        session: AsyncSession,
        user: User,
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDCDonation()
