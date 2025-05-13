from typing import Generic, TypeVar, List

from pydantic import BaseModel

T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    total: int
    limit: int
    offset: int
    data: List[T]