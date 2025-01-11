from sqlalchemy import select
from backend.api_v1.users.models_sql import UserWeights
from backend.core.dao import BaseDAO
from backend.core.database_sql import async_session


class UserWeightsDAO(BaseDAO[UserWeights]):
    model = UserWeights
    
    @classmethod
    async def get_by_user_id(cls, user_id: int):
        async with async_session() as session:
            query = (
                select(cls.model).where(cls.model.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        