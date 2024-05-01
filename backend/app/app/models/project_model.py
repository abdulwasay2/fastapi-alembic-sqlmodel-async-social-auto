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


class LimitsBase(SQLModel):
    daily_swipe_limit: int | None
    daily_match_limit: int | None
    daily_conversations_limit: int | None
    daily_messages_limit: int | None


class DelaysBase(SQLModel):
    response_delay: int | None
    followup_delay: int | None 
    open_profile_delay: int | None
    delay_before_message: int | None


class SwipeSettingsBase(SQLModel):
    gender_preferences: str = "male"
    age_range_start: int | None
    age_range_end: int | None
    swipe_right_ratio: int | None
    swipe_delay: int | None


class ChattingSettingsBase(SQLModel):
    target_platform: str
    target_handle: str
    custom_cta: str = "male"
    messages_before_handle: int | None
    begin_chatting_every: int | None
    no_old_conversations_messages: int | None


class GeneralSettingsBase(SQLModel):
    block_images: bool = False
    sleep_duration: int | None
    random_naps: int | None



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


class Limits(BaseUUIDModel, LimitsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Limits.project_id==Project.id",
        }
    )


class Delays(BaseUUIDModel, DelaysBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Delays.project_id==Project.id",
        }
    )



class SwipeSettings(BaseUUIDModel, SwipeSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "SwipeSettings.project_id==Project.id",
        }
    )


class ChattingSettings(BaseUUIDModel, ChattingSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ChattingSettings.project_id==Project.id",
        }
    )


class GeneralSettings(BaseUUIDModel, GeneralSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "GeneralSettings.project_id==Project.id",
        }
    )