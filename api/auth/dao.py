from sqlalchemy import select as sqlalchemy_select

from api.dao.base import BaseDAO
from api.database import async_session_maker
from api.auth.models import TokenBlacklist


class TokenBlacklistDAO(BaseDAO):
    model = TokenBlacklist

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> TokenBlacklist | None:
        async with async_session_maker() as session:
            query = sqlalchemy_select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
