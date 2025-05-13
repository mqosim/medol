from sqlalchemy.ext.asyncio import AsyncSession

from src.medol.core.security import get_password_hash
from src.medol.models.user_model import User
from src.medol.repositories.user_repository import UserRepository
from src.medol.schemas.user_schema import UserCreate, UserUpdate
from src.medol.services.base_service import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, UserRepository(session), session)

    async def create(self, data: UserCreate, unique_fields: list[str] | None = None) -> User:
        data.password = get_password_hash(data.password)

        return await super().create(data=data, unique_fields=unique_fields)
