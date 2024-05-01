from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import project_deps
from app.models.project_model import Project
from app.models.user_model import User
from app.schemas.project_schema import (
    IProjectCreate,
    IProjectRead,
    IProjectUpdate,
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
    NameExistException,
)
from sqlmodel import SQLModel, select, func


router = APIRouter()


@router.get("")
async def get_project(
    params: Params = Depends(),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IGetResponsePaginated[IProjectRead]:
    """
    Gets a paginated list of project
    """
    my_query = select(Project).where(Project.user_id == current_user.id)
    project = await crud.project.get_multi_paginated(query=my_query, params=params)
    return create_response(data=project)


@router.get("/{project_id}")
async def get_project_by_id(
    project_id: UUID,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IGetResponseBase[IProjectRead]:
    """
    Gets a project by its id
    """
    project = await crud.project.get(id=project_id, user_id=current_user.id)
    if project:
        return create_response(data=project)
    else:
        raise IdNotFoundException(Project, project_id)


@router.post("")
async def create_project(
    project: IProjectCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[IProjectRead]:
    """
    Creates a new project

    Required roles:
    - admin
    - manager
    """
    project_current = await crud.project.get_project_by_name(name=project.name, current_user=current_user)
    if project_current:
        raise NameExistException(Project, name=project.name)
    new_project = await crud.project.create(obj_in=project, user_id=current_user.id)
    return create_response(data=new_project)


@router.put("/{project_id}")
async def update_project(
    project: IProjectUpdate,
    current_project: Project = Depends(project_deps.get_project_by_id),
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[IProjectRead]:
    """
    Updates a project by its id

    Required roles:
    - admin
    - manager
    """
    project_updated = await crud.project.update(obj_current=current_project, obj_new=project)
    return create_response(data=project_updated)
