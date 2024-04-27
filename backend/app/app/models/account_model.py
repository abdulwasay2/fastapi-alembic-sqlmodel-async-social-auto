from app.models.organization_model import Organization
from sqlmodel import SQLModel as SQLModel, Field, Relationship, Enum


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    organization_id: int | None = Field(default=None, foreign_key="organization.id")
    organization: Organization | None = Relationship(back_populates="related_organization")
    # space id is what?
    proxy: str | None
    gender: Enum[GenderEnum]
    is_banned : bool = Field(default=False)
    age: int
    name: str | None
    location: str | None
    language: str | None = Field(default='en')
    is_verified : bool = Field(default=True)
    # image_ids is what?
    bio: str | None
