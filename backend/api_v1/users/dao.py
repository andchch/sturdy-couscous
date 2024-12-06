from typing import Optional, List
from sqlalchemy import select

from backend.api_v1.games.models_sql import Achievement
from backend.core.dao import BaseDAO
from backend.api_v1.users.models_sql import User, UserInteraction
from backend.core.database_sql import async_session

class AchievementDAO(BaseDAO[Achievement]):
    model = Achievement
    
    @classmethod
    async def get_by_app_steam_id(cls, appid: str, steamid: str, achievement: str) -> Optional[Achievement]:
        async with async_session() as session:
            query = select(cls.model).where(cls.model.appid == appid,
                                            cls.model.steamid == steamid,
                                            cls.model.achievement == achievement)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        

class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_by_email(cls, email: str) -> Optional[User]:
        async with async_session() as session:
            query = select(cls.model).where(cls.model.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_username(cls, username: str) -> Optional[User]:
        async with async_session() as session:
            query = select(cls.model).where(cls.model.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get_by_steamid(cls, steamid: str) -> Optional[User]:  
        async with async_session() as session:
            query = select(cls.model).where(cls.model.steamid == steamid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

class UserInteractionDAO(BaseDAO[UserInteraction]):
    model = UserInteraction

    @classmethod
    async def get_user_interactions(cls, user_id: int) -> List[UserInteraction]:
        async with async_session() as session:
            query = select(cls.model).where(
                (cls.model.user_1_id == user_id) | 
                (cls.model.user_2_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create_interaction(
        cls, 
        user_1_id: int, 
        user_2_id: int, 
        game: str,
        user_1_rating: int,
        user_2_rating: int
    ) -> UserInteraction:
        return await cls.create(
            user_1_id=user_1_id,
            user_2_id=user_2_id,
            game=game,
            user_1_rating=user_1_rating,
            user_2_rating=user_2_rating
        ) 