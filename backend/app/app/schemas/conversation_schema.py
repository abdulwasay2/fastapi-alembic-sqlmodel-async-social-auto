from app.models.conversation_model import ConversationBase
from app.utils.partial import optional
from uuid import UUID


class IConversationCreate(ConversationBase):
    pass


@optional()
class IConversationUpdate(ConversationBase):
    pass


class IConversationRead(ConversationBase):
    id: UUID

