from fastapi import APIRouter

from src.medol.api.endpoints import user_route, file_route

api_router = APIRouter()

api_router.include_router(user_route.router, prefix="/users", tags=["users"])
api_router.include_router(file_route.router, prefix="/files", tags=["files"])