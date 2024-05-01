from app.models.organization_model import OrganizationBase
from app.utils.partial import optional
from uuid import UUID


class IOrganizationCreate(OrganizationBase):
    pass


@optional()
class IOrganizationUpdate(OrganizationBase):
    pass


class IOrganizationRead(OrganizationBase):
    id: UUID

