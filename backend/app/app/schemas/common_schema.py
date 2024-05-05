from uuid import UUID
from app.utils.uuid6 import uuid7
from pydantic import BaseModel, field_validator
from enum import Enum


class IGenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class IStatusEnum(str, Enum):
    pause = "pause"
    running = "running"
    deleted = "deleted"


class IConversationStatusEnum(str, Enum):
    open = "open"
    closed = "closed"


class ITargetPlatformEnum(str, Enum):
    snapchat = "snapchat"
    instagram = "instagram"
    facebook = "facebook"
    whatsapp = "whatsapp"
    twitter = "twitter"
    google = "google"


class IUserMessage(BaseModel):
    """User message schema."""

    user_id: UUID | None = None
    message: str


class IChatResponse(BaseModel):
    """Chat response schema."""

    id: str
    message_id: str
    sender: str
    message: str
    type: str

    @field_validator("id", "message_id")
    def check_ids(cls, v):
        if v == "" or v is None:
            return str(uuid7())
        return v

    @field_validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @field_validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
