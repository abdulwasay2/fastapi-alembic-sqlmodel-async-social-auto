from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship, Column, String
from app.models.base_uuid_model import BaseUUIDModel
from app.schemas.common_schema import IGenderEnum, IStatusEnum, ITargetPlatformEnum
# from app.models.user_model import User
from sqlalchemy_utils import ChoiceType


class ProjectBase(SQLModel):
    name: str
    status: IStatusEnum = Field(
        default=IStatusEnum.running,
        sa_column=Column(ChoiceType(IStatusEnum, impl=String())),
    )
    platform: ITargetPlatformEnum = Field(
        default=ITargetPlatformEnum.google,
        sa_column=Column(ChoiceType(ITargetPlatformEnum, impl=String())),
    )


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
    gender_preferences: IGenderEnum | None = Field(
        default=IGenderEnum.other,
        sa_column=Column(ChoiceType(IGenderEnum, impl=String())),
    )
    age_range_start: int | None
    age_range_end: int | None
    swipe_right_ratio: int | None
    swipe_delay: int | None


class ChattingSettingsBase(SQLModel):
    target_platform: str
    target_handle: str
    custom_cta: str = "msg me please, I'm busy"
    unmatch_after_handle: bool = False
    messages_before_handle: int | None
    begin_chatting_every: int | None
    no_old_conversations_messages: int | None


class GeneralSettingsBase(SQLModel):
    block_images: bool = False
    sleep_duration: int | None
    random_naps: int | None


class Project(BaseUUIDModel, ProjectBase, table=True):
    user_id: UUID = Field(foreign_key="User.id")
    # user: User = Relationship(
    #     sa_relationship_kwargs={
    #         "lazy": "joined",
    #         "primaryjoin": "Project.user_id==User.id",
    #     }
    # )
    limits: list["Limits"] = Relationship(
        back_populates="project", 
        sa_relationship_kwargs={'lazy': 'selectin'})
    delays: list["Delays"] = Relationship(
        back_populates="project", 
        sa_relationship_kwargs={'lazy': 'selectin'})
    swipe_settings: list["SwipeSettings"] = Relationship(
        back_populates="project", 
        sa_relationship_kwargs={'lazy': 'selectin'})
    chatting_settings: list["ChattingSettings"] = Relationship(
        back_populates="project", 
        sa_relationship_kwargs={'lazy': 'selectin'})
    general_settings: list["GeneralSettings"] = Relationship(
        back_populates="project", 
        sa_relationship_kwargs={'lazy': 'selectin'})


class Limits(BaseUUIDModel, LimitsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Limits.project_id==Project.id",
            "cascade": "delete"
        }
    )


class Delays(BaseUUIDModel, DelaysBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Delays.project_id==Project.id",
            "cascade": "delete"
        }
    )



class SwipeSettings(BaseUUIDModel, SwipeSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "SwipeSettings.project_id==Project.id",
            "cascade": "delete"
        }
    )


class ChattingSettings(BaseUUIDModel, ChattingSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ChattingSettings.project_id==Project.id",
            "cascade": "delete"
        }
    )


class GeneralSettings(BaseUUIDModel, GeneralSettingsBase, table=True):
    project_id: UUID = Field(foreign_key="Project.id")
    project: Project = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "GeneralSettings.project_id==Project.id",
            "cascade": "delete"
        }
    )