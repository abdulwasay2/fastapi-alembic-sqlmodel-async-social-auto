from app import crud
from app.models.conversation_model import Conversation
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_conversation_by_id(
    conversation_id: Annotated[UUID, Path(description="The UUID id of the conversation")]
) -> Conversation:
    conversation = await crud.conversation.get(id=conversation_id)
    if not conversation:
        raise IdNotFoundException(Conversation, id=conversation_id)
    return conversation
