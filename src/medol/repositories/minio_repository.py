import io
import os
import uuid
from datetime import timedelta
from typing import List, BinaryIO, Tuple

from minio import Minio
from minio.error import S3Error

from src.medol.repositories.file_storage_repository import FileStorageRepository


class MinioRepository(FileStorageRepository):

    def __init__(
            self,
            minio_client: Minio,
            bucket_name: str
    ):
        self.client = minio_client
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file_data: BinaryIO, file_name: str, content_type: str) -> str:
        try:
            file_data.seek(0, os.SEEK_END)
            file_size = file_data.tell()
            file_data.seek(0)

            file_path = f"{uuid.uuid4().hex}/{file_name}"

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_path,
                data=file_data,
                length=file_size,
                content_type=content_type
            )

            return file_path
        except S3Error as e:
            raise Exception(f"MinIO store error: {str(e)}")

    def download_file(self, file_path: str) -> Tuple[BinaryIO, str]:
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=file_path
            )

            file_data = io.BytesIO(response.data)
            content_type = response.headers.get('Content-Type', 'application/octet-stream')

            return file_data, content_type
        except S3Error as e:
            raise Exception(f"File not found: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=file_path
            )
            return True
        except S3Error as e:
            raise Exception(f"Delete file error: {str(e)}")

    def list_files(self, prefix: str = "") -> List[str]:
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=True
            )

            return [obj.object_name for obj in objects]
        except S3Error as e:
            raise Exception(f"List files error: {str(e)}")

    def get_file_url(self, file_path: str, expires=timedelta(minutes=30)) -> str:
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=file_path,
                expires=expires
            )
            return url
        except S3Error as e:
            raise Exception(f"Get URL error: {str(e)}")
