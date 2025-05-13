import os
from typing import List, Optional

from fastapi import HTTPException, status, UploadFile

MAX_FILE_SIZE_MB = 5


class FileValidator:

    def __init__(
            self,
            allowed_types: Optional[List[str]] = None,
            max_size_mb: float = 50.0
    ):
        self.allowed_types = allowed_types or [
            "image/jpeg", "image/png", "image/gif",
            "application/pdf", "text/plain",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]
        self.max_size_bytes = int(max_size_mb * 1024 * 1024)

    def validate_file_type(self, file: UploadFile) -> bool:
        content_type = file.content_type

        if content_type not in self.allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"This file type is not allowed. Allowed types: {', '.join(self.allowed_types)}"
            )

        return True

    def validate_file_size(self, file: UploadFile) -> bool:
        file_size = len(file.file.read())
        file.file.seek(0)

        max_file_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

        if file_size > max_file_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB."
            )

        return True

    def get_unique_filename(self, filename: str) -> str:
        name, ext = os.path.splitext(filename)
        timestamp = int(os.path.getmtime(filename)) if os.path.exists(filename) else 0
        return f"{name}_{timestamp}{ext}"

    def validate(self, file: UploadFile) -> bool:
        return (
                self.validate_file_type(file) and
                self.validate_file_size(file)
        )
