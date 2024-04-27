from uuid import UUID
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel as SQLModel, Field, Relationship, Enum, Column, Dict, JSON
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User


class StatusEnum(str, Enum):
    PAUSE = "pause"
    RUNNING = "running"
    DELETED = "deleted"


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    platform: str
    status: Enum[StatusEnum]
    limits: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    delays: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    swipe_settings: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    chatting_settings: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    general_settings: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="related_user")

    class Config:
        arbitrary_types_allowed = True
