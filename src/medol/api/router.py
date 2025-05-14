from fastapi import APIRouter, Depends

from src.medol.api.endpoints import user_route, file_route, auth_route
from src.medol.dependencies.dependencies import get_current_user

api_router = APIRouter()

api_router.include_router(auth_route.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_route.router, prefix="/users", tags=["users"])
api_router.include_router(file_route.router, prefix="/files", tags=["files"], dependencies=[Depends(get_current_user)])