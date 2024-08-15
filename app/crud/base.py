from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.user import User
from app.services.donation import donate_to_project

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model) -> None:
        self.model = model

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
        self, attr_name, attr_value, session: AsyncSession
    ) -> Optional[ModelType]:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        user: Optional[User],
        session: AsyncSession,
    ) -> Optional[ModelType]:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def apply_donation(
        self,
        db_obj: ModelType,
        session: AsyncSession
    ) -> ModelType:
        db_obj = await donate_to_project(
            new_obj=db_obj,
            session=session,
        )
        await session.commit()
        await session.refresh(db_obj)
        return db_obj