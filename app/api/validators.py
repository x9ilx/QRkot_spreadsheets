from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exist(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    db_charity_project = await session.execute(
        select(CharityProject).where(CharityProject.id == charity_project_id)
    )
    db_charity_project = db_charity_project.scalars().first()
    if db_charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найден',
        )
    return db_charity_project


async def check_charity_project_name_duplicate(
    project_name: str, session: AsyncSession
) -> None:
    project = await charity_project_crud.get_by_attribute(
        attr_name='name',
        attr_value=project_name,
        session=session,
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_havent_deposit(
    charity_project: CharityProject,
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_charity_project_full_amount_greater_invested_amount(
    charity_project: CharityProject,
    new_full_amount_value: int,
) -> None:
    if charity_project.invested_amount > new_full_amount_value:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя установить значение full_amount меньше '
                'уже вложенной суммы.'
            ),
        )


async def check_charity_project_not_fully_invested(
    charity_project: CharityProject,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя изменить закрытый проект.'),
        )
