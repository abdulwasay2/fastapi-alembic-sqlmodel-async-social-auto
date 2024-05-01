from app.models.organization_model import Organization
from app.schemas.organization_schema import IOrganizationUpdate, IOrganizationCreate
from app.crud.base_crud import CRUDBase
from sqlmodel import select
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDOrganization(CRUDBase[Organization, IOrganizationCreate, IOrganizationUpdate]):
    async def get_organization_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Organization:
        db_session = db_session or super().get_db().session
        organization = await db_session.execute(select(Organization).where(Organization.name == name))
        return organization.scalar_one_or_none()

organization = CRUDOrganization(Organization)
