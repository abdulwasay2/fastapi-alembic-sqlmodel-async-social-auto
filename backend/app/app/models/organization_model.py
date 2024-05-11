from sqlmodel import SQLModel as SQLModel, Relationship
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_model import User



class OrganizationBase(SQLModel):
    name: str


class Organization(BaseUUIDModel, OrganizationBase, table=True):
    users: list["User"] = Relationship(
        sa_relationship_kwargs={'lazy': 'selectin'})
