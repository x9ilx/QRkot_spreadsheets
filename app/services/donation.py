from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.mixins import DonationMixIn
from app.services.base import close_donation_or_project


async def donate_to_project(
    new_obj: DonationMixIn,
    session: AsyncSession,
):
    apply_object_type = (
        CharityProject if type(new_obj) == Donation else Donation
    )
    while not new_obj.fully_invested:
        apply_object = await session.execute(
            select(apply_object_type)
            .where(apply_object_type.fully_invested == false())
            .order_by(apply_object_type.create_date)
        )
        apply_object = apply_object.scalars().first()
        if apply_object is None:
            break
        if apply_object_type is CharityProject:
            charity_project, donation = apply_object, new_obj
        else:
            charity_project, donation = new_obj, apply_object
        left_to_pay = (
            charity_project.full_amount - charity_project.invested_amount
        )
        remaining_balance = donation.full_amount - donation.invested_amount
        add_sum = (
            remaining_balance
            if remaining_balance <= left_to_pay
            else left_to_pay
        )
        donation.invested_amount += add_sum
        charity_project.invested_amount += add_sum
        if donation.full_amount == donation.invested_amount:
            donation = close_donation_or_project(donation)
        if charity_project.full_amount == charity_project.invested_amount:
            charity_project = close_donation_or_project(charity_project)
    return new_obj
