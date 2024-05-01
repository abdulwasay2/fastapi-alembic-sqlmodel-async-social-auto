from app.models.account_model import Account
from app.models.user_model import User
from app.schemas.account_schema import IAccountCreate, IAccountUpdate
from app.crud.base_crud import CRUDBase
from sqlmodel import select
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDAccount(CRUDBase[Account, IAccountCreate, IAccountUpdate]):
    async def get_account_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Account:
        db_session = db_session or super().get_db().session
        account = await db_session.execute(select(Account).where(Account.name == name))
        return account.scalar_one_or_none()

account = CRUDAccount(Account)
