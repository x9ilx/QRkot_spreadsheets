from sqlalchemy import extract, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.datetime import convert_seconds_to_dhms


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    def __init__(self) -> None:
        super().__init__(CharityProject)

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        project_closing_time = (
            extract('epoch', CharityProject.close_date) -
            extract('epoch', CharityProject.create_date)
        ).label('project_closing_time')
        charity_projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.description,
                project_closing_time,
            )
            .filter(CharityProject.fully_invested == true())
            .order_by(project_closing_time)
        )
        result = []
        for row in charity_projects:
            result.append(
                {
                    'name': row.name,
                    'description': row.description,
                    'project_closing_time': convert_seconds_to_dhms(
                        row.project_closing_time
                    ),
                }
            )
        return result


charity_project_crud = CRUDCharityProject()
