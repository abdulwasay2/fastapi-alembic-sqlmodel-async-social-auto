from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import organization_deps
from app.models.organization_model import Organization
from app.models.user_model import User
from app.schemas.organization_schema import (
    IOrganizationCreate,
    IOrganizationRead,
    IOrganizationUpdate,
)
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.utils.exceptions import (
    IdNotFoundException,
    NameExistException,
)

router = APIRouter()


@router.get("")
async def get_organization(
    params: Params = Depends()
) -> IGetResponsePaginated[IOrganizationRead]:
    """
    Gets a paginated list of organization
    """
    organization = await crud.organization.get_multi_paginated(params=params)
    return create_response(data=organization)


@router.get("/{organization_id}")
async def get_organization_by_id(
    organization_id: UUID
) -> IGetResponseBase[IOrganizationRead]:
    """
    Gets a organization by its id
    """
    organization = await crud.organization.get(id=organization_id)
    if organization:
        return create_response(data=organization)
    else:
        raise IdNotFoundException(Organization, organization_id)


@router.post("")
async def create_organization(
    organization: IOrganizationCreate
) -> IPostResponseBase[IOrganizationRead]:
    """
    Creates a new organization
    """
    organization_current = await crud.organization.get_organization_by_name(name=organization.name)
    if organization_current:
        raise NameExistException(Organization, name=organization.name)
    # new_organization = await crud.organization.create(obj_in=organization, created_by_id=current_user.id)
    new_organization = await crud.organization.create(obj_in=organization)
    return create_response(data=new_organization)


@router.put("/{organization_id}")
async def update_organization(
    organization: IOrganizationUpdate,
    current_organization: Organization = Depends(organization_deps.get_organization_by_id)
) -> IPutResponseBase[IOrganizationRead]:
    """
    Updates a organization by its id
    """
    organization_updated = await crud.organization.update(
        obj_current=current_organization, obj_new=organization)
    return create_response(data=organization_updated)


@router.delete("/{organization_id}")
async def remove_organization(
    organization_id: UUID,
) -> IDeleteResponseBase[IOrganizationRead]:
    """
    Deletes a organization by its id
    """
    organization = await crud.organization.get(id=organization_id)
    if not organization:
        raise IdNotFoundException(Organization, organization_id)
    organization = await crud.organization.remove(id=organization_id)
    return create_response(data=organization)
