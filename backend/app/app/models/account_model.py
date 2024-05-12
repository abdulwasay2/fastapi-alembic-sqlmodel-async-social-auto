from uuid import UUID
from typing import List
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel, Field, Relationship, Column, JSON, ARRAY, String, ForeignKey
from app.models.base_uuid_model import BaseUUIDModel
from app.schemas.common_schema import IGenderEnum
from app.models.organization_model import Organization
from sqlalchemy_utils import ChoiceType


class AccountBase(SQLModel):
    name: str
    proxy: str | None
    gender: IGenderEnum | None = Field(
        default=IGenderEnum.other,
        sa_column=Column(ChoiceType(IGenderEnum, impl=String())),
    )
    age: int | None
    location: str | None
    language: str = "en"
    bio: str | None
    valid_proxy: bool = Field(default=False)
    organization_id: UUID = ForeignKey("Organization.id")
    credentials: dict = None
    image_ids: List[str] = Field(default=[], sa_column=Column(ARRAY(String())))
    platform: str = Field(default="google", nullable=False)


class Account(BaseUUIDModel, AccountBase, table=True):
    # space_id  (fk is missing)
    # image_ids (fk is missing)

    credentials: dict = Field(sa_column=Column(JSON), default_factory=dict)
    is_banned: bool = Field(default=False)
    is_verified: bool = Field(default=True)
    organization_id: UUID = Field(foreign_key="Organization.id")
    organization: Organization = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Account.organization_id==Organization.id",
        }
    )
