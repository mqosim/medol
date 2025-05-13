from typing import List, Optional

from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    file_name: str
    file_url: Optional[str] = None


class FileList(BaseModel):
    files: List[str] = Field(default_factory=list)
