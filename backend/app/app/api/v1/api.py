from fastapi import APIRouter
from app.api.v1.endpoints import (
    organization,
    project,
    account,
    conversation
)

api_router = APIRouter()
api_router.include_router(organization.router, prefix="/organization", tags=["organization"])
api_router.include_router(project.router, prefix="/project", tags=["project"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(conversation.router, prefix="/conversation", tags=["conversation"])
