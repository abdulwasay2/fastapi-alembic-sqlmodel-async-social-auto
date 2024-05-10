from app.models.base_uuid_model import BaseUUIDModel
from app.models.organization_model import Organization
from app.models.links_model import LinkGroupUser
from app.schemas.common_schema import IGenderEnum
from datetime import datetime
from sqlmodel import BigInteger, Field, SQLModel, Relationship, Column, DateTime, String
from typing import Optional
from sqlalchemy_utils import ChoiceType
from pydantic import EmailStr
from uuid import UUID


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    role_id: UUID | None = Field(default=None, foreign_key="Role.id")


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str | None = Field(default=None, nullable=False, index=True)
    role: Optional["Role"] = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )
    groups: list["Group"] = Relationship(  # noqa: F821
        back_populates="users",
        link_model=LinkGroupUser,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    organization_id: UUID | None = Field(default=None, foreign_key="Organization.id")
    organization: Organization = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "User.organization_id==Organization.id",
        }
    )