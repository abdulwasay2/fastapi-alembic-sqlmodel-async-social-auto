from app.models.conversation_model import ConversationBase
from app.utils.partial import optional
from uuid import UUID
from sqlmodel import SQLModel


class IConversationCreate(ConversationBase):
    status: str
    account_id: UUID


@optional()
class IConversationUpdate(ConversationBase):
    pass


class IConversationRead(ConversationBase):
    id: UUID

