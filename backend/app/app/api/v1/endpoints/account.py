from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.deps import account_deps
from app.models.account_model import Account
from app.models.user_model import User
from app.schemas.account_schema import (
    IAccountCreate,
    IAccountRead,
    IAccountUpdate,
)
from app.schemas.response_schema import (
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
from app.api.celery_task import increment, validate_account_credentials, validate_account_proxy

router = APIRouter()


@router.get("")
async def get_account(
    params: Params = Depends()
) -> IGetResponsePaginated[IAccountRead]:
    """
    Gets a paginated list of account
    """
    account = await crud.account.get_multi_paginated(params=params)
    return create_response(data=account)


@router.get("/{account_id}")
async def get_account_by_id(
    account_id: UUID
) -> IGetResponseBase[IAccountRead]:
    """
    Gets a account by its id
    """
    account = await crud.account.get(id=account_id)
    if account:
        return create_response(data=account)
    else:
        raise IdNotFoundException(Account, account_id)


@router.post("")
async def create_account(
    account: IAccountCreate
) -> IPostResponseBase[IAccountRead]:
    """
    Creates a new account
    """
    account_current = await crud.account.get_account_by_name(name=account.name)
    if account_current:
        raise NameExistException(Account, name=account.name)
    # new_account = await crud.account.create(obj_in=account, created_by_id=current_user.id)
    new_account = await crud.account.create(obj_in=account)
    return create_response(data=new_account)


@router.put("/{account_id}")
async def update_account(
    account: IAccountUpdate,
    current_account: Account = Depends(account_deps.get_account_by_id)
) -> IPutResponseBase[IAccountRead]:
    """
    Updates a account by its id
    """
    account_updated = await crud.account.update(obj_current=current_account, obj_new=account)
    return create_response(data=account_updated)


@router.post("/validate_proxy/{account_id}")
async def validate_account(
    account_id: UUID,
):
    """
    Validates the account proxy
    """

    print(account_id)
    validate_account_proxy.delay(account_id)
    return {"message": "task queued"}


@router.post("/validate/{account_id}")
async def validate_account(
    account_id: UUID,
):
    """
    Validates the account credentials and proxy
    """
    print(account_id)
    validate_account_proxy(account_id)
    validate_account_credentials.delay(account_id)
    return {"message": "task queued"}