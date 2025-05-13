from typing import TypeVar, Generic, Type, Any

from pydantic import BaseModel
from sqlalchemy import select, UUID, func
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: BaseModel) -> T:
        item = data.model_dump(exclude_unset=True)
        db_item = self.model(**item)
        self.session.add(db_item)
        await self.session.flush()
        await self.session.refresh(db_item)

        return db_item

    async def get_by_id(self, item_id: int) -> T | None:
        stmt = select(self.model).where(item_id == self.model.id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_uuid(self, uuid: UUID) -> T | None:
        stmt = select(self.model).where(uuid == self.model.uuid)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def update_by_id(self, item_id: int, data: BaseModel) -> T:
        db_item = await self._stmt_by_id(item_id)

        return await self._db_item(db_item, "ID", item_id, data)

    async def update_by_uuid(self, item_uuid: UUID, data: BaseModel) -> T:
        db_item = await self._stmt_by_uuid(item_uuid)

        return await self._db_item(db_item, "UUID", item_uuid, data)

    async def get_all(self, limit: int = 10, offset: int = 0) -> tuple[list[T], int]:
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        total_stmt = select(func.count()).select_from(self.model)
        total_result = await self.session.execute(total_stmt)
        total = total_result.scalar_one()

        return list(items), total

    async def delete_by_id(self, item_id: int) -> bool:
        item = await self.get_by_id(item_id)
        if not item:
            return False

        await self.session.delete(item)
        await self.session.flush()

        return True

    async def delete_by_uuid(self, uuid: UUID) -> bool:
        item = await self.get_by_uuid(uuid)
        if not item:
            return False

        await self.session.delete(item)
        await self.session.flush()

        return True

    async def _stmt_by_uuid(self, uuid: UUID):
        stmt = select(self.model).where(uuid == self.model.uuid)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def _stmt_by_id(self, item_id: int):
        stmt = select(self.model).where(item_id == self.model.id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def _db_item(self, db_item: Any, title: str, item_id: T, data: BaseModel):
        if not db_item:
            raise ValueError(f"{self.model.__name__} with {title} {item_id} not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(db_item, field, value)

        await self.session.flush()
        await self.session.refresh(db_item)
        return db_item