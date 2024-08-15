from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationDB,
                                  DonationDBForSuperuser)


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    return await donation_crud.apply_donation(
        db_obj=await donation_crud.create(donation, user, session),
        session=session,
    )


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    return await donation_crud.get_user_donation(session, user)


@router.get(
    '/',
    response_model=list[DonationDBForSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_all(session=session)
