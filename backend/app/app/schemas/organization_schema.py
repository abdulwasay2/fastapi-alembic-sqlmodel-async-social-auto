from app.models.organization_model import OrganizationBase
from app.models.user_model import UserBase, UserProjectBase
from app.utils.partial import optional
from uuid import UUID
from sqlmodel import SQLModel


class IOrganizationCreate(OrganizationBase):
    pass


@optional()
class IOrganizationUpdate(OrganizationBase):
    pass


class IOrganizationRead(OrganizationBase):
    id: UUID


class IOrganizationDetailsRead(SQLModel):
    id: UUID
    name: str
    users: list[UserProjectBase]