from app.models.base_uuid_model import BaseUUIDModel
# from app.models.organization_model import Organization
from app.models.links_model import LinkGroupUser
from sqlmodel import Field, SQLModel, Relationship, Column, String
from typing import Optional
from pydantic import EmailStr
from uuid import UUID
from app.models.project_model import Project
from app.schemas.project_schema import IProjectRead


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
    projects: list["Project"] = Relationship(  # noqa: F821
        sa_relationship_kwargs={"lazy": "joined"}
    )

    # TODO: Fix the circular dependency b/w user and organization to add below join

    # organization = Relationship(
    #     sa_relationship_kwargs={
    #         "lazy": "joined",
    #         "primaryjoin": "User.organization_id==Organization.id",
    #     }
    # )


class UserProjectBase(SQLModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    projects: list[IProjectRead]