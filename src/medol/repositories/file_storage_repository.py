from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List, BinaryIO, Tuple


class FileStorageRepository(ABC):

    @abstractmethod
    def upload_file(self, file_data: BinaryIO, file_name: str, content_type: str) -> str:
        pass

    @abstractmethod
    def download_file(self, file_path: str) -> Tuple[BinaryIO, str]:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def list_files(self, prefix: str = "") -> List[str]:
        pass

    @abstractmethod
    def get_file_url(self, file_path: str, expires: timedelta) -> str:
        pass
