from uuid import UUID
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel as SQLModel, Field
from app.models.base_uuid_model import BaseUUIDModel



class Organization(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str