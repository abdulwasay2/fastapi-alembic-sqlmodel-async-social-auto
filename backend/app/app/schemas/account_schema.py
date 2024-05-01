from app.models.account_model import AccountBase
from app.utils.partial import optional
from uuid import UUID


class IAccountCreate(AccountBase):
    pass


@optional()
class IAccountUpdate(AccountBase):
    pass


class IAccountRead(AccountBase):
    id: UUID

