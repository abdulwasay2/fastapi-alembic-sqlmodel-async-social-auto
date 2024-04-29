from app import crud
from app.models.organization_model import Organization
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_organization_by_name(
    organization_name: Annotated[
        str, Query(description="String compare with name or last name")
    ] = ""
) -> str:
    organization = await crud.organization.get_organization_by_name(name=organization_name)
    if not organization:
        raise NameNotFoundException(Organization, name=organization_name)
    return organization


async def get_organization_by_id(
    organization_id: Annotated[UUID, Path(description="The UUID id of the organization")]
) -> Organization:
    organization = await crud.organization.get(id=organization_id)
    if not organization:
        raise IdNotFoundException(Organization, id=organization_id)
    return organization
