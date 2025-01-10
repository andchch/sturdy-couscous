from typing import Optional
from sqlalchemy import select
from backend.api_v1.external_integration.models_sql import SteamProfile
from backend.core.database_sql import async_session
from backend.core.dao import BaseDAO


class SteamProfileDAO(BaseDAO[SteamProfile]):
    model = SteamProfile
    
    @staticmethod
    async def get_by_user_id(cls, user_id: int) -> Optional[SteamProfile]:
        async with async_session() as session:
            query = (
                select(cls.model).where(SteamProfile.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        