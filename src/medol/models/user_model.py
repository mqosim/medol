from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from src.medol.models.base_model import Base, TimestampMixin, UUIDMixin


class User(Base, TimestampMixin, UUIDMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
