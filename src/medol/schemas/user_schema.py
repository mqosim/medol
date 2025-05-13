import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreate(UserBase):
    password: str
    avatar: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserOut(UserBase):
    id: int
    uuid: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
