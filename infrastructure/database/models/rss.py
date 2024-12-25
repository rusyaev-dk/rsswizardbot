from typing import Optional

from sqlalchemy import String, BOOLEAN
from sqlalchemy import text, BIGINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base, TimestampMixin


class RSSLocal(Base, TimestampMixin):
    __tablename__ = "rss"

    rss_id: Mapped[str] = mapped_column(String(255), primary_key=True, autoincrement=False)
    rss_url: Mapped[str] = mapped_column(String(512), primary_key=False, autoincrement=False)
    owner_tg_id: Mapped[int] = mapped_column(BIGINT, primary_key=False, autoincrement=False)
