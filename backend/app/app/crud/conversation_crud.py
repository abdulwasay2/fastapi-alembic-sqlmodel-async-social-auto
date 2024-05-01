from app.models.conversation_model import Conversation
from app.models.user_model import User
from app.schemas.conversation_schema import IConversationCreate, IConversationUpdate
from app.crud.base_crud import CRUDBase
from sqlmodel import select
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDConversation(CRUDBase[Conversation, IConversationCreate, IConversationUpdate]):
    async def get_conversation_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Conversation:
        db_session = db_session or super().get_db().session
        conversation = await db_session.execute(select(Conversation).where(Conversation.id == id))
        return conversation.scalar_one_or_none()

conversation = CRUDConversation(Conversation)
