from uuid import UUID
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, String
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User
from sqlalchemy_utils import ChoiceType



class IStatusEnum(str, Enum):
    pause = "pause"
    running = "running"
    deleted = "deleted"


class ProjectBase(SQLModel):
    name: str


class Project(BaseUUIDModel, ProjectBase, table=True):
    platform: str = Field(default="tinder", nullable=False)
    status: str = Field(default="running", nullable=False)
    user_id: UUID = Field(foreign_key="User.id")
    user: User = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Project.user_id==User.id",
        }
    )
