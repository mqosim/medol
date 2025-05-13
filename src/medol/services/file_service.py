import io
import os
from datetime import timedelta
from typing import Dict, Any, Tuple, List, BinaryIO, Optional

from fastapi import HTTPException, UploadFile, status

from src.medol.repositories.file_storage_repository import FileStorageRepository
from src.medol.utils.file_validator import FileValidator


class FileService:

    def __init__(self, repository: FileStorageRepository, validator: Optional[FileValidator] = None):
        self.repository = repository
        self.validator = validator or FileValidator()

    async def upload_file(self, file: UploadFile) -> Dict[str, Any]:
        try:
            self.validator.validate(file)

            file_content = await file.read()
            file_io = io.BytesIO(file_content)

            file_path = self.repository.upload_file(
                file_data=file_io,
                file_name=file.filename,
                content_type=file.content_type or "application/octet-stream"
            )

            url = self.get_file_url(file_path)

            return {
                "file_name": file_path,
                "file_url": url
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def download_file(self, file_path: str) -> Tuple[BinaryIO, str, str]:
        try:
            file_data, content_type = self.repository.download_file(file_path)
            file_name = os.path.basename(file_path)
            return file_data, content_type, file_name
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

    def delete_file(self, file_path: str) -> Dict[str, Any]:
        try:
            success = self.repository.delete_file(file_path)
            return {
                "success": success,
                "message": "File deleted successfully"
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def list_files(self, prefix: str = "") -> List[str]:
        try:
            return self.repository.list_files(prefix)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def get_file_url(self, file_path: str, expires: timedelta = timedelta(minutes=30)) -> str:
        try:
            return self.repository.get_file_url(file_path, expires)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )