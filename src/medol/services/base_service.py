from typing import TypeVar, Generic, Type
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


class BaseService(Generic[T, C, U]):
    def __init__(self, model: Type[T], repo, session: AsyncSession):
        self.model = model
        self.repo = repo
        self.session = session

    async def create(self, data: C, unique_fields: list[str] | None = None) -> T:
        try:
            if unique_fields:
                for field in unique_fields:
                    value = getattr(data, field, None)
                    if value is not None:
                        check_method = getattr(self.repo, f"get_by_{field}", None)
                        if check_method:
                            existing = await check_method(value)
                            if existing:
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"{self.model.__name__} with this {field} already exists.",
                                )

            created = await self.repo.create(data)
            await self.session.commit()
            return created

        except Exception as e:
            await self.session.rollback()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating {self.model.__name__.lower()}: {str(e)}"
            )

    async def get_by_id(self, item_id: int, model_name: str) -> T | None:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_name} not found",
            )

        return item

    async def get_by_uuid(self, item_uuid: UUID, model_name: str) -> T | None:
        item = await self.repo.get_by_uuid(item_uuid)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_name} not found",
            )

        return item

    async def get_all(self, limit: int = 10, offset: int = 0) -> tuple[list[T], int]:
        return await self.repo.get_all(limit=limit, offset=offset)

    async def update_by_id(self, item_id: int, data: U, model_name: str, unique_fields: list[str] | None = None) -> T:
        try:
            existing_item = await self.repo.get_by_id(item_id)
            await self._existing_item_and_unique_field_checking(existing_item, data, model_name, unique_fields)

            update_item = await self.repo.update_by_id(item_id, data)
            await self.session.commit()

            return update_item

        except Exception as e:
            await self.session.rollback()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating {model_name}: {str(e)}",
            )

    async def update_by_uuid(self, item_uuid: UUID, data: U, model_name: str,
                             unique_fields: list[str] | None = None) -> T:
        try:
            existing_item = await self.repo.get_by_uuid(item_uuid)
            await self._existing_item_and_unique_field_checking(existing_item, data, model_name, unique_fields)

            update_item = await self.repo.update_by_uuid(item_uuid, data)
            await self.session.commit()

            return update_item

        except Exception as e:
            await self.session.rollback()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating {model_name}: {str(e)}",
            )

    async def delete_by_id(self, item_id: int) -> None:
        try:
            result = await self.repo.delete_by_id(item_id)
            if result:
                await self.session.commit()

        except Exception as e:
            if isinstance(e, HTTPException):
                await self.session.rollback()

                raise e

    async def delete_by_uuid(self, item_uuid: UUID) -> None:
        try:
            result = await self.repo.delete_by_uuid(item_uuid)
            if result:
                await self.session.commit()

        except Exception as e:
            if isinstance(e, HTTPException):
                await self.session.rollback()

                raise e

    async def _existing_item_and_unique_field_checking(self, existing_item: T, data: U, model_name: str,
                                                       unique_fields: list[str] | None = None):
        if existing_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model_name} not found",
            )

        if unique_fields:
            for unique_field in unique_fields:
                existing_value = getattr(existing_item, unique_field, None)
                new_value = getattr(data, unique_field, None)

                if new_value and existing_value != new_value:
                    check_method = getattr(self.repo, f"get_by_{unique_field}", None)
                    if check_method:
                        conflict_item = await check_method(new_value)
                        if conflict_item:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"{model_name} with this {unique_field} already exists",
                            )