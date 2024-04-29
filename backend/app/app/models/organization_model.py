from sqlmodel import SQLModel as SQLModel
from app.models.base_uuid_model import BaseUUIDModel



class OrganizationBase(SQLModel):
    name: str


class Organization(BaseUUIDModel, OrganizationBase, table=True):
    pass