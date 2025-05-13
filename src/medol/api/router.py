from fastapi import APIRouter

from src.medol.api.endpoints import user_route

api_router = APIRouter()

api_router.include_router(user_route.router, prefix="/users", tags=["users"])