from uuid import UUID
from app.models.account_model import Account
from sqlmodel import SQLModel, Field, JSON, Relationship
from app.models.base_uuid_model import BaseUUIDModel
from pydantic import BaseModel


class MessagesDetails(BaseModel):
    role: str
    message: str


class ConversationBase(SQLModel):
    account_id: UUID
    # messages: list[MessagesDetails] | None
    fan_name: str
    fan_url: str = "https://tinder.com"


class Conversation(BaseUUIDModel, ConversationBase, table=True):
    status: str = Field(default="active")
    # messages: JSON
    account_id: UUID = Field(foreign_key="Account.id")
    account: Account = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Conversation.account_id==Account.id",
        }
    )
