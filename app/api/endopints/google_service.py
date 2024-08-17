from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    create_spreadsheet,
    set_user_permissions,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_repost(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
):
    charity_projects = (
        await charity_project_crud.get_projects_by_completion_rate(session)
    )
    spreadsheet_id = await create_spreadsheet(wrapper_service)
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(
        spreadsheet_id, charity_projects, wrapper_service
    )
    return charity_projects
