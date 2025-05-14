from fastapi import APIRouter, status, Query, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.medol.db.config import get_async_session
from src.medol.dependencies.dependencies import oauth2_scheme, get_current_user
from src.medol.schemas.user_schema import UserOut, UserCreate, UserUpdate
from src.medol.services.user_service import UserService
from src.medol.utils.pagination import PaginationResponse

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_async_session)) -> UserOut:
    async with session.begin():
        service = UserService(session)
        created_user = await service.create(data=data, unique_fields=["email"])

    return UserOut.model_validate(created_user)


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                   current_user: str = Depends(get_current_user)) -> UserOut:
    async with session.begin():
        service = UserService(session)
        user = await service.get_by_id(item_id=user_id, model_name="user")

    return UserOut.model_validate(user)


@router.get("/{user_id}/avatar", status_code=status.HTTP_200_OK)
async def get_avatar(user_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: str = Depends(get_current_user)):
    async with session.begin():
        service = UserService(session)
        avatar_url = await service.get_avatar(user_id)

    return {"url": avatar_url}


@router.get("/", response_model=PaginationResponse[UserOut], status_code=status.HTTP_200_OK)
async def list_users(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0),
                     session: AsyncSession = Depends(get_async_session), current_user: str = Depends(get_current_user)) -> \
PaginationResponse[UserOut]:
    async with session.begin():
        service = UserService(session)
        users, total = await service.get_all(limit=limit, offset=offset)

    return PaginationResponse(
        total=total,
        limit=limit,
        offset=(offset // limit) + 1,
        data=users,
    )


@router.put("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(get_current_user)) -> UserOut:
    async with session.begin():
        service = UserService(session)
        user = await service.update_by_id(item_id=user_id, data=data, model_name="user", unique_fields=["email"])

    return UserOut.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session),
                      current_user: str = Depends(get_current_user)):
    async with session.begin():
        service = UserService(session)
        await service.delete_by_id(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
