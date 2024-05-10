from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import project_deps
from app.models.project_model import ChattingSettings, Delays, Limits, Project, SwipeSettings, GeneralSettings
from app.models.user_model import User
from app.schemas.project_schema import (
    IProjectCreate,
    IProjectDetailsRead,
    IProjectRead,
    IProjectUpdate,
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
from sqlmodel import SQLModel, select, func


router = APIRouter()


@router.get("")
async def get_project(
    params: Params = Depends(),
) -> IGetResponsePaginated[IProjectRead]:
    """
    Gets a paginated list of project
    """
    # my_query = select(Project).where(Project.user_id == current_user.id)
    project = await crud.project.get_multi_paginated(params=params)
    return create_response(data=project)


@router.get("/{project_id}")
async def get_project_by_id(
    project_id: UUID
) -> IGetResponseBase[IProjectDetailsRead]:
    """
    Gets a project by its id
    """
    project = await crud.project.get(id=project_id)
    if project:
        return create_response(data=project)
    else:
        raise IdNotFoundException(Project, project_id)


@router.post("")
async def create_project(
    project: IProjectCreate
) -> IPostResponseBase[IProjectCreate]:
    """
    Creates a new project
    """
    project_current = await crud.project.get_project_by_name(
        name=project.name, current_user=project.user_id)
    if project_current:
        raise NameExistException(Project, name=project.name)
    if not await crud.user.get(id=project.user_id):
        raise IdNotFoundException(User, project.user_id)
    new_project = await crud.project.create(obj_in=project)
    return create_response(data=new_project)


@router.put("/{project_id}")
async def update_project(
    project: IProjectUpdate,
    current_project: Project = Depends(project_deps.get_project_by_id)
) -> IPutResponseBase[IProjectDetailsRead]:
    """
    Updates a project by its id
    """
    if project.user_id and not await crud.user.get(id=project.user_id):
        raise IdNotFoundException(User, project.user_id)

    project = project.model_dump(exclude_defaults=True, exclude_none=True)
    limits = project.pop("limits", None)
    if limits:
        prev_limit = select(Limits).where(Limits.project_id==current_project.id)
        prev_limit = await crud.project.db.session.execute(prev_limit)
        prev_limit = prev_limit.scalar_one_or_none()
        await crud.project.update(obj_current=prev_limit, obj_new=limits[0])

    delays = project.pop("delays", None)
    if delays:
        prev_delay = select(Delays).where(Delays.project_id==current_project.id)
        prev_delay = await crud.project.db.session.execute(prev_delay)
        prev_delay = prev_delay.scalar_one_or_none()
        await crud.project.update(obj_current=prev_delay, obj_new=delays[0])

    chatting_settings = project.pop("chatting_settings", None)
    if chatting_settings:
        prev_chatting_setting = select(ChattingSettings).where(ChattingSettings.project_id==current_project.id)
        prev_chatting_setting = await crud.project.db.session.execute(prev_chatting_setting)
        prev_chatting_setting = prev_chatting_setting.scalar_one_or_none()
        await crud.project.update(obj_current=prev_chatting_setting, obj_new=chatting_settings[0])

    swipe_settings = project.pop("swipe_settings", None)
    if swipe_settings:
        prev_swipe_setting = select(SwipeSettings).where(SwipeSettings.project_id==current_project.id)
        prev_swipe_setting = await crud.project.db.session.execute(prev_swipe_setting)
        prev_swipe_setting = prev_swipe_setting.scalar_one_or_none()
        await crud.project.update(obj_current=prev_swipe_setting, obj_new=swipe_settings[0])

    general_settings = project.pop("general_settings", None)
    if general_settings:
        prev_general_setting = select(GeneralSettings).where(GeneralSettings.project_id==current_project.id)
        prev_general_setting = await crud.project.db.session.execute(prev_general_setting)
        prev_general_setting = prev_general_setting.scalar_one_or_none()
        await crud.project.update(obj_current=prev_general_setting, obj_new=general_settings[0])

    project_updated = await crud.project.update(obj_current=current_project, obj_new=project)
    return create_response(data=project_updated)


@router.delete("/{project_id}")
async def remove_project(
    project_id: UUID,
) -> IDeleteResponseBase[IProjectDetailsRead]:
    """
    Deletes a project by its id
    """
    project = await crud.project.get(id=project_id)
    if not project:
        raise IdNotFoundException(Project, project_id)
    project = await crud.project.remove(id=project_id)
    return create_response(data=project)