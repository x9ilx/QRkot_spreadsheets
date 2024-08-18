from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.mixins import DonationMixIn
from app.services.base import close_donation_or_project


async def donate_to_project(
    new_obj: DonationMixIn,
    session: AsyncSession,
):
    if type(new_obj) == Donation:
        crud_apply_object, crud_new_obj = charity_project_crud, donation_crud
    else:
        crud_apply_object, crud_new_obj = donation_crud, charity_project_crud
    while not new_obj.fully_invested:
        apply_object = await crud_apply_object.get_first_not_fully_invested(
            session
        )
        if apply_object is None:
            break
        if apply_object is CharityProject:
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
            close_donation_or_project(donation)
        if charity_project.full_amount == charity_project.invested_amount:
            close_donation_or_project(charity_project)
    return await crud_new_obj.accept_all_changes(new_obj, session)
