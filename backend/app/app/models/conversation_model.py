from uuid import UUID
from app.models.account_model import Account
from sqlmodel import SQLModel, Field, JSON, Relationship, Column, String
from app.schemas.common_schema import IConversationStatusEnum
from app.models.base_uuid_model import BaseUUIDModel
from sqlalchemy_utils import ChoiceType
from pydantic import BaseModel


class MessagesDetails(BaseModel):
    role: str
    message: str


class ConversationBase(SQLModel):
    account_id: UUID
    messages: dict | None = Field(sa_column=Column(JSON), default_factory=dict)
    fan_name: str
    fan_url: str = "https://tinder.com"


class Conversation(BaseUUIDModel, ConversationBase, table=True):
    status: str = Field(
        default=IConversationStatusEnum.open,
        sa_column=Column(ChoiceType(IConversationStatusEnum, impl=String())),
    )
    account_id: UUID = Field(foreign_key="Account.id")
    account: Account = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Conversation.account_id==Account.id",
        }
    )
