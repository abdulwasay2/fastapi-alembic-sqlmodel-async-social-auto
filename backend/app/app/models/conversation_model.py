from app.models.account_model import Account
from app.models.fan_model import Fan
from sqlmodel import SQLModel, Field, Relationship, Enum


class StatusEnum(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class Coversation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    account_id: int | None = Field(default=None, foreign_key="account.id")
    account: Account | None = Relationship(back_populates="conversation_account")
    status: Enum[StatusEnum]
    fan_id: int | None = Field(default=None, foreign_key="fan.id")
    fan: Fan | None = Relationship(back_populates="related_fan")
    # messages is what?
    fan_name: str | None
    fan_url: str | None
