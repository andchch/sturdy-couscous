from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from backend.api_v1.communities.models_sql import Community, CommunityMembership
from backend.core.dao import BaseDAO

from backend.core.database_sql import async_session


class CommunityDAO(BaseDAO[Community]):
    model = Community
    
    @classmethod
    async def get_by_name(cls, name: str) -> Optional[Community]:
        async with async_session() as session:
            query = select(cls.model).where(cls.model.name == name)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get(cls, offset, limit) -> list[Community]:
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.members))
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
        
        
class CommunityMembershipDAO(BaseDAO[CommunityMembership]):
    model = CommunityMembership
    
    @classmethod
    async def get_user_membership(cls, user_id, community_id):
        async with async_session() as session:
            query = select(cls.model).where(
                cls.model.user_id == user_id,
                cls.model.community_id == community_id,
                )
            result = await session.execute(query)
            return result.scalar_one_or_none()