from typing import Optional

from sqlalchemy import String, BOOLEAN
from sqlalchemy import text, BIGINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    language: Mapped[str] = mapped_column(String(10), server_default=text("'ru'"))
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True, autoincrement=False)

    def __repr__(self):
        return f"<User {self.telegram_id} {self.username} {self.full_name}>"
