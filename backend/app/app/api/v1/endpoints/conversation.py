from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import conversation_deps, user_deps
from app.models.conversation_model import Conversation
from app.models.user_model import User
from app.schemas.conversation_schema import (
    IConversationCreate,
    IConversationRead,
    IConversationUpdate,
)
from app.schemas.response_schema import (
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.utils.exceptions import (
    IdNotFoundException,
)

router = APIRouter()


@router.get("")
async def get_conversation(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IConversationRead]:
    """
    Gets a paginated list of conversation
    """
    conversation = await crud.conversation.get_multi_paginated(params=params)
    return create_response(data=conversation)


@router.get("/{conversation_id}")
async def get_conversation_by_id(
    conversation_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IConversationRead]:
    """
    Gets a conversation by its id
    """
    conversation = await crud.conversation.get(id=conversation_id)
    if conversation:
        return create_response(data=conversation)
    else:
        raise IdNotFoundException(Conversation, conversation_id)


@router.post("")
async def create_conversation(
    conversation: IConversationCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[IConversationRead]:
    """
    Creates a new conversation

    Required roles:
    - admin
    - manager
    """
    new_conversation = await crud.conversation.create(obj_in=conversation)
    return create_response(data=new_conversation)


@router.put("/{conversation_id}")
async def update_conversation(
    conversation: IConversationUpdate,
    current_conversation: Conversation = Depends(conversation_deps.get_conversation_by_id),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[IConversationRead]:
    """
    Updates a conversation by its id

    Required roles:
    - admin
    - manager
    """
    conversation_updated = await crud.conversation.update(obj_current=current_conversation, obj_new=conversation)
    return create_response(data=conversation_updated)