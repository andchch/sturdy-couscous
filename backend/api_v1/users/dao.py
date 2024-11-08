from typing import Optional, List
from sqlalchemy import select

from core.dao import BaseDAO
from api_v1.users.models_sql import User, UserProfile, UserInteraction
from core.database_sql import async_session

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
    # TODO: check
class UserProfileDAO(BaseDAO[UserProfile]):
    model = UserProfile

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> Optional[UserProfile]:
        async with async_session() as session:
            query = select(cls.model).join(User).where(User.id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_weights(cls, profile_id: int, **weights) -> Optional[UserProfile]:
        return await cls.update(profile_id, **weights)

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