from app import crud
from app.models.account_model import Account
from app.utils.exceptions.common_exception import (
    NameNotFoundException,
    IdNotFoundException,
)
from uuid import UUID
from fastapi import Query, Path
from typing_extensions import Annotated


async def get_account_by_name(
    account_name: Annotated[
        str, Query(description="String compare with name or last name")
    ] = ""
) -> str:
    account = await crud.account.get_account_by_name(name=account_name)
    if not account:
        raise NameNotFoundException(Account, name=account_name)
    return account


async def get_account_by_id(
    account_id: Annotated[UUID, Path(description="The UUID id of the account")]
) -> Account:
    account = await crud.account.get(id=account_id)
    if not account:
        raise IdNotFoundException(Account, id=account_id)
    return account
