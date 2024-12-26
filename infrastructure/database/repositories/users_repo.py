from typing import Optional

from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import UserLocal


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_user(
            self,
            telegram_id: int,
            full_name: str,
            language_code: str,
            username: Optional[str] = None,
    ) -> UserLocal:
        stmt = (
            insert(UserLocal)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                language_code=language_code,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=[UserLocal.telegram_id],
                set_={
                    "full_name": full_name,
                    "language_code": language_code,
                    "username": username
                }
            )
            .returning(UserLocal)
        )
        result = await self.__session.execute(stmt)
        await self.__session.commit()

        return result.scalar_one()

    async def get_user(self, telegram_id: int) -> Optional[UserLocal]:
        stmt = select(UserLocal).where(UserLocal.telegram_id == telegram_id)
        result = await self.__session.scalar(stmt)
        return result

    async def get_users_count_by_language(self, language_code: str) -> int:
        stmt = select(func.count(UserLocal.telegram_id)).where(
            and_(UserLocal.is_active == True, UserLocal.language_code == language_code)
        )
        result = await self.__session.scalar(stmt)
        return result or 0

    async def get_user_language_code(self, telegram_id: int) -> str:
        stmt = select(UserLocal.language_code).where(UserLocal.telegram_id == telegram_id)
        result = await self.__session.scalar(stmt)
        return result

    async def get_users(self, *clauses) -> list[UserLocal]:
        stmt = select(UserLocal).where(*clauses)
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def get_active_users_count(self) -> int:
        stmt = select(func.count(UserLocal.telegram_id)).where(UserLocal.is_active == True)
        result = await self.__session.scalar(stmt)
        return result or 0

    async def get_users_count(self) -> int:
        stmt = select(func.count(UserLocal.telegram_id))
        result = await self.__session.scalar(stmt)
        return result or 0

    async def update_user(
            self,
            *clauses,
            **values,
    ) -> None:
        stmt = update(UserLocal).where(*clauses).values(**values)
        await self.__session.execute(stmt)
        await self.__session.commit()
