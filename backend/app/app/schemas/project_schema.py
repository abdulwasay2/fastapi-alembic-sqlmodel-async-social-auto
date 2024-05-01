from app.models.project_model import (
    ProjectBase, 
    LimitsBase,
    DelaysBase,
    SwipeSettingsBase,
    ChattingSettingsBase,
    GeneralSettingsBase,
)
from app.utils.partial import optional
from uuid import UUID
from sqlmodel import SQLModel


class IProjectCreate(SQLModel):
    name: str
    user_id: UUID
    limits: LimitsBase
    delays: DelaysBase
    swipe_settings: SwipeSettingsBase
    chatting_settings: ChattingSettingsBase
    general_settings: GeneralSettingsBase


@optional()
class IProjectUpdate(ProjectBase):
    pass


class IProjectRead(SQLModel):
    id: UUID
    name: str

