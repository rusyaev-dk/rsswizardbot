from typing import Optional

from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserDBRepo(BaseRepo):
    async def add_user(
            self,
            telegram_id: int,
            full_name: str,
            language: str,
            username: Optional[str] = None,
    ) -> User:
        stmt = (
            insert(User)
            .values(
                telegram_id=telegram_id,
                full_name=full_name,
                language=language,
                username=username,
            )
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_={
                    "full_name": full_name,
                    "language": language,
                    "username": username
                }
            )
            .returning(User)
        )
        result = await self.session.execute(stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get_user(
            self,
            telegram_id: int
    ) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.scalar(stmt)
        return result

    async def get_user_language_code(
            self,
            telegram_id: int
    ) -> str:
        stmt = select(User.language).where(User.telegram_id == telegram_id)
        result = await self.session.scalar(stmt)
        return result

    async def get_all_users(
            self,
            language_code: str = None
    ):
        if language_code:
            stmt = select(User).where(User.language == language_code)
        else:
            stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_users_count(self) -> int:
        stmt = select(func.count(User.telegram_id))
        result = await self.session.scalar(stmt)
        return result

    async def get_active_users_count(self) -> int:
        stmt = select(func.count(User.telegram_id)).where(User.is_active == True)
        result = await self.session.scalar(stmt)
        return result

    async def get_users_count_by_language(self, language_code: str) -> int:
        stmt = select(func.count(User.telegram_id)).where(
            and_(
                User.language == language_code,
                User.is_active == True
            )
        )
        result = await self.session.scalar(stmt)
        return result

    async def update_user(
            self,
            *clauses,
            **values,
    ):
        stmt = update(User).where(*clauses).values(**values)
        await self.session.execute(stmt)
        await self.session.commit()
