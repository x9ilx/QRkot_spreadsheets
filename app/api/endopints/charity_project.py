from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exist,
    check_charity_project_full_amount_greater_invested_amount,
    check_charity_project_havent_deposit, check_charity_project_name_duplicate,
    check_charity_project_not_fully_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.base import close_donation_or_project


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_charity_project_name_duplicate(
        project_name=charity_project.name, session=session
    )
    return await charity_project_crud.apply_donation(
        db_obj=await charity_project_crud.create(
            obj_in=charity_project,
            session=session,
            user=None,
        ),
        session=session,
    )


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exist(
        charity_project_id, session
    )
    await check_charity_project_not_fully_invested(charity_project)
    if obj_in.name is not None:
        await check_charity_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_charity_project_full_amount_greater_invested_amount(
            charity_project,
            obj_in.full_amount,
        )
        if charity_project.invested_amount == obj_in.full_amount:
            charity_project = close_donation_or_project(charity_project)
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
    charity_project_id: int, session: AsyncSession = Depends(get_async_session)
):
    db_charity_project = await check_charity_project_exist(
        charity_project_id, session
    )
    await check_charity_project_havent_deposit(db_charity_project)
    return await charity_project_crud.delete(db_charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_all(session=session)
