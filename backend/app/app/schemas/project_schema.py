from app.models.project_model import (
    ProjectBase, 
    Limits,
    Delays,
    SwipeSettings,
    ChattingSettings,
    GeneralSettings,
    LimitsBase,
    DelaysBase,
    SwipeSettingsBase,
    ChattingSettingsBase,
    GeneralSettingsBase,
)
from app.utils.partial import optional
from app.schemas.common_schema import IStatusEnum, ITargetPlatformEnum
from uuid import UUID
from sqlmodel import SQLModel


class IProjectCreate(SQLModel):
    name: str
    user_id: UUID
    platform: ITargetPlatformEnum
    limits: list[Limits]
    delays: list[Delays]
    swipe_settings: list[SwipeSettings]
    chatting_settings: list[ChattingSettings]
    general_settings: list[GeneralSettings]


@optional()
class IProjectUpdate(IProjectCreate):
    pass


class IProjectRead(SQLModel):
    id: UUID
    name: str


@optional()
class IProjectDetailsRead(SQLModel):
    name: str
    user_id: UUID
    status: IStatusEnum
    platform: ITargetPlatformEnum
    limits: list[LimitsBase]
    delays: list[DelaysBase]
    swipe_settings: list[SwipeSettingsBase]
    chatting_settings: list[ChattingSettingsBase]
    general_settings: list[GeneralSettingsBase]
