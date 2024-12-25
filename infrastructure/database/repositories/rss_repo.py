from typing import Optional

from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.api.clients.rss_client import RSSClient
from infrastructure.api.models.rss import RSS
from infrastructure.database.models.rss import RSSLocal
from tgbot.services.micro_functions import generate_random_id


class RSSRepository:
    def __init__(
            self,
            session: AsyncSession,
            rss_client: RSSClient
    ):
        self.__session = session
        self.__rss_client = rss_client

    async def add_rss(
            self,
            rss_url: str,
            owner_tg_id: int
    ) -> RSSLocal:
        stmt = (
            insert(RSSLocal)
            .values(
                rss_id=generate_random_id(30),
                rss_url=rss_url,
                owner_tg_id=owner_tg_id
            )
            .on_conflict_do_update(
                index_elements=[RSSLocal.rss_id],
                set_={
                    "owner_tg_id": owner_tg_id,
                    "rss_url": rss_url
                }
            )
            .returning(RSSLocal)
        )
        result = await self.__session.execute(stmt)
        await self.__session.commit()

        return result.scalar_one()

    async def get_all_user_rss(self, owner_tg_id: int) -> list[RSS]:
        stmt = select(RSSLocal).where(RSSLocal.owner_tg_id == owner_tg_id)
        result = await self.__session.execute(stmt)
        rss_local_list = result.scalars().all() or []

        return [RSS.from_local(rss_local) for rss_local in rss_local_list]

    async def delete_rss(self, owner_tg_id: int, rss_id: str) -> None:
        stmt = delete(RSSLocal).where(and_(RSSLocal.owner_tg_id == owner_tg_id, RSSLocal.rss_id == rss_id))
        await self.__session.execute(stmt)
        await self.__session.commit()

    async def get_rss_by_id(self, rss_id: str) -> Optional[RSS]:
        stmt = select(RSSLocal).where(RSSLocal.rss_id == rss_id)
        result = await self.__session.execute(stmt)
        rss_local = result.scalar_one_or_none()

        return RSS.from_local(rss_local) if rss_local else None

    async def get_rss_entries(self, rss_url: str) -> tuple[list[dict], int]:
        entries, status_code = await self.__rss_client.get_entries(rss_url)
        return entries, status_code

    async def validate_rss(self, rss_url: str) -> tuple[bool, int]:
        valid, status_code = await self.__rss_client.validate_rss(rss_url)
        return valid, status_code

    async def is_rss_exists(self, owner_tg_id: int, rss_url) -> bool:
        user_rss_list = await self.get_all_user_rss(owner_tg_id)
        if not len(user_rss_list):
            return False

        for rss in user_rss_list:
            if rss_url == rss.rss_url:
                return True

        return False
