import os

from src.medol.core.config import Settings
from src.medol.repositories.minio_repository import MinioRepository
from src.medol.services.file_service import FileService


def get_minio_repository() -> MinioRepository:
    minio_client = Settings.get_minio_client()
    return MinioRepository(
        minio_client=minio_client,
        bucket_name=os.getenv("MINIO_BUCKET_NAME", "fastapi-files")
    )


def get_file_service() -> FileService:
    repository = get_minio_repository()
    return FileService(repository=repository)
