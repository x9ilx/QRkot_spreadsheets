from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    def __init__(self) -> None:
        super().__init__(CharityProject)


charity_project_crud = CRUDCharityProject()
