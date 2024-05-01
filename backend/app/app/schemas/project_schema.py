from app.models.project_model import ProjectBase
from app.utils.partial import optional
from uuid import UUID


class IProjectCreate(ProjectBase):
    user_id: UUID | None = None


@optional()
class IProjectUpdate(ProjectBase):
    pass


class IProjectRead(ProjectBase):
    id: UUID

