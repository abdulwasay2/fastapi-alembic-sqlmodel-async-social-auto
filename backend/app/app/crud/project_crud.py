from app.models.project_model import Project
from app.schemas.project_schema import IProjectUpdate, IProjectCreate
from app.crud.base_crud import CRUDBase
from sqlmodel import select
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDProject(CRUDBase[Project, IProjectCreate, IProjectUpdate]):
    async def get_project_by_name(
        self, *, name: str, db_session: AsyncSession | None = None, current_user=None,
    ) -> Project:
        db_session = db_session or super().get_db().session

        project = await db_session.execute(select(Project).where(Project.name == name, Project.user_id == current_user))
        return project.scalar_one_or_none()

project = CRUDProject(Project)
