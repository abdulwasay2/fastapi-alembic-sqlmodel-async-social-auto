from app.models.account_model import AccountBase
from app.utils.partial import optional
from uuid import UUID
# from pydantic import field_validator
# from app.db.session import SessionLocal


# async def get_existing(uuid):
#     async with SessionLocal() as session:
#         await asyncio.sleep(5)  # Add a delay of 5 seconds
#         account = await crud.organization.get(id=uuid, db_session=session)
#         return account


class IAccountCreate(AccountBase):
    pass
    
    # @field_validator("organization_id")
    # async def validate_fk_existence(cls, v):
    #     ins = get_existing(v)
    #     if ins:
    #         return v
    #     return f"{cls.__name__} with id {v} does not exist"


@optional()
class IAccountUpdate(AccountBase):
    pass


class IAccountRead(AccountBase):
    id: UUID

