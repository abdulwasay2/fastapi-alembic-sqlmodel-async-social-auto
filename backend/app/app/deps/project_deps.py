from app import crud
from app.models.project_model import Project
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_project_by_name(
    project_name: Annotated[
        str, Query(description="String compare with name or last name")
    ] = ""
) -> str:
    project = await crud.project.get_project_by_name(name=project_name)
    if not project:
        raise NameNotFoundException(Project, name=project_name)
    return project


async def get_project_by_id(
    project_id: Annotated[UUID, Path(description="The UUID id of the project")]
) -> Project:
    project = await crud.project.get(id=project_id)
    if not project:
        raise IdNotFoundException(Project, id=project_id)
    return project
