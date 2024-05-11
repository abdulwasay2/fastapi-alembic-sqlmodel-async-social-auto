from fastapi import HTTPException
from typing import Any, Generic, TypeVar
from uuid import UUID
from app.schemas.common_schema import IOrderEnum
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params, Page
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func, exists
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select
from sqlalchemy import exc

from ..models.project_model import (
    Limits,
    Delays,
    SwipeSettings,
    ChattingSettings,
    GeneralSettings,
    
)

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get_db(self) -> type(db):
        return self.db

    async def get(
        self, *, id: UUID | str, db_session: AsyncSession | None = None, user_id: UUID = None,
    ) -> ModelType | None:
        db_session = db_session or self.db.session
        if user_id:
            query = select(self.model).where(self.model.id == id, self.model.user_id == user_id)
        else:
            query = select(self.model).where(self.model.id == id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()
    
    async def exists(
        self, *, id: UUID | str, db_session: AsyncSession | None = None,
    ) -> ModelType | None:
        db_session = db_session or self.db.session
        query = select(exists().where(self.model.id == id))
        response = await db_session.execute(query)
        return response.scalar()

    async def get_by_ids(
        self,
        *,
        list_ids: list[UUID | str],
        db_session: AsyncSession | None = None,
    ) -> list[ModelType] | None:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_count(
        self, db_session: AsyncSession | None = None
    ) -> ModelType | None:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> list[ModelType]:
        db_session = db_session or self.db.session
        if query is None:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_multi_paginated(
        self,
        *,
        params: Params | None = Params(),
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        db_session = db_session or self.db.session
        if query is None:
            query = select(self.model)

        output = await paginate(db_session, query, params)
        return output

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Params | None = Params(),
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        db_session = db_session or self.db.session

        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = "id"

        if query is None:
            if order == IOrderEnum.ascendent:
                query = select(self.model).order_by(columns[order_by].asc())
            else:
                query = select(self.model).order_by(columns[order_by].desc())

        return await paginate(db_session, query, params)

    async def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.ascendent,
        db_session: AsyncSession | None = None,
    ) -> list[ModelType]:
        db_session = db_session or self.db.session

        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = "id"

        if order == IOrderEnum.ascendent:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by].desc())
            )

        response = await db_session.execute(query)
        return response.scalars().all()

    async def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        created_by_id: UUID | str | None = None,
        user_id: UUID | str | None = None,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        db_session = db_session or self.db.session
        if user_id:
            obj_in.user_id = user_id

        db_obj = self.model.model_validate(obj_in)  # type: ignore

        if created_by_id:
            db_obj.created_by_id = created_by_id

        if user_id:
            db_obj.user_id = user_id

        try:
            db_session.add(db_obj)
            await db_session.commit()
            obj_id = db_obj.id

            child_objects = []
            obj_in = obj_in.dict()
            if "limits" in obj_in:
                limits = obj_in.pop("limits")
                limits[0]["project_id"] = obj_id
                db_limits = Limits(**limits[0])
                # child_objects.append(db_limits)

            if "delays" in obj_in:
                delays = obj_in.pop("delays")
                delays[0]["project_id"] = obj_id
                db_delays = Delays(**delays[0])
                # child_objects.append(db_delays)

            if "chatting_settings" in obj_in:
                chatting_settings = obj_in.pop("chatting_settings")
                print(chatting_settings[0], "\n\n\n")
                chatting_settings[0]["project_id"] = obj_id
                db_chatting_settings = ChattingSettings(**chatting_settings[0])
                # child_objects.append(db_chatting_settings)

            if "swipe_settings" in obj_in:
                swipe_settings = obj_in.pop("swipe_settings")
                swipe_settings[0]["project_id"] = obj_id
                db_swipe_settings = SwipeSettings(**swipe_settings[0])
                # child_objects.append(db_swipe_settings)

            if "general_settings" in obj_in:
                general_settings = obj_in.pop("general_settings")
                general_settings[0]["project_id"] = obj_id
                db_general_settings = GeneralSettings(**general_settings[0])
                # child_objects.append(db_general_settings)

            if child_objects:
                # Add all child objects to the session
                db_session.add_all(child_objects)
                # Commit the session
                await db_session.commit()

        except exc.IntegrityError:
            from traceback import print_exc
            print_exc()
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType,
        db_session: AsyncSession | None = None,
    ) -> ModelType:
        db_session = db_session or self.db.session

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def remove(
        self, *, id: UUID | str, db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj
