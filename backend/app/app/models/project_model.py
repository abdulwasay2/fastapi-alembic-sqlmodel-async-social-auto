from uuid import UUID
from app.utils.uuid6 import uuid7
from sqlmodel import SQLModel, Field, Relationship, Enum, Column, BigInteger
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User
from sqlalchemy_utils import ChoiceType


class IStatusEnum(str, Enum):
    pause = "pause"
    running = "running"
    deleted = "deleted"


class IGenderEnum(str, Enum):
    male = "male"
    female = "female"


class ITargetPlatform(str, Enum):
    snapchat = "snapchat"
    instagram = "instagram"
    facebook = "facebook"
    whatsapp = "whatsapp"
    twitter = "twitter"


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


class Limits(BaseUUIDModel, SQLModel, table=True):
    daily_swipe_limit: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    daily_match_limit: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    daily_conversations_limit: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    daily_messages_limit: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Limit.project_id==Project.id",
        }
    )


class Delays(BaseUUIDModel, SQLModel, table=True):
    response_delay: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    followup_delay: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    open_profile_delay: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    delay_before_message: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Delays.project_id==Project.id",
        }
    )



class SwipeSettings(BaseUUIDModel, SQLModel, table=True):
    gender_preferences: str = Field(default="male", nullable=False)
    age_range_start: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    age_range_end: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    swipe_right_ratio: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    swipe_delay: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "SwipeSettings.project_id==Project.id",
        }
    )


class ChattingSettings(BaseUUIDModel, SQLModel, table=True):
    target_platform: str = Field(nullable=False)
    target_handle: str = Field(nullable=False)
    custom_cta: str = Field(default="male", nullable=False)
    messages_before_handle: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    begin_chatting_every: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    no_old_conversations_messages: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ChattingSettings.project_id==Project.id",
        }
    )


class GeneralSettings(BaseUUIDModel, SQLModel, table=True):
    block_images: bool = Field(default=False)
    sleep_duration: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    random_naps: int | None = Field(
        default=None, sa_column=Column(BigInteger(), server_default="0")
    )
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "GeneralSettings.project_id==Project.id",
        }
    )