import os

from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.medol.core.config import Settings
from src.medol.db.config import get_async_session
from src.medol.repositories.minio_repository import MinioRepository
from src.medol.services.auth_service import AuthService
from src.medol.services.file_service import FileService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        service = AuthService(session)

    try:
        email = await service.verify_token(token)
        return email
    except (ExpiredSignatureError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_minio_repository() -> MinioRepository:
    minio_client = Settings.get_minio_client()
    return MinioRepository(
        minio_client=minio_client,
        bucket_name=os.getenv("MINIO_BUCKET_NAME", "fastapi-files")
    )


def get_file_service() -> FileService:
    repository = get_minio_repository()
    return FileService(repository=repository)
