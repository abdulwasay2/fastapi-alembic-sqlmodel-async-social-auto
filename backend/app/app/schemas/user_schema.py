from app.models.user_model import UserBase
from app.utils.partial import optional
from uuid import UUID
from pydantic import BaseModel


class IUserCreate(UserBase):
    password: str

    class Config:
        hashed_password = None


# All these fields are optional
@optional()
class IUserUpdate(UserBase):
    pass


class IUserBasicInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str