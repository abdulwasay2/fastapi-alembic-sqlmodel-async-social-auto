from uuid import UUID
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, BigInteger
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User
from app.models.organization_model import Organization



class AccountBase(SQLModel):
    name: str
    proxy: str | None
    gender: str = "male"
    age: int | None
    location: str | None
    language: str = "en"
    bio: str | None
    organization_id: UUID = None


class Account(BaseUUIDModel, AccountBase, table=True):
    # space_id  (fk is missing)
    # image_ids (fk is missing)

    platform: str = Field(default="tinder", nullable=False)
    is_banned: bool = Field(default=False)
    is_verified: bool = Field(default=True)
    organization_id: UUID = Field(foreign_key="Organization.id")
    organization: Organization = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Account.organization_id==Organization.id",
        }
    )
