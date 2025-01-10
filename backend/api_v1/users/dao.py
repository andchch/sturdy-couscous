from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from backend.api_v1.external_integration.models_sql import SteamProfile
from backend.api_v1.games.models_sql import Achievement
from backend.core.dao import BaseDAO
from backend.api_v1.users.models_sql import User, UserContacts, UserFollow, UserInteraction
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
            query = ( 
                select(cls.model)
                .where(cls.model.email == email)
                .options(
                    joinedload(User.contacts)
                    )
            )
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
        
    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session() as session:
            query = (
                select(cls.model).where(cls.model.id == model_id)
                .options(
                    joinedload(User.integro)
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

        
    @classmethod
    async def update_contacts(cls, user_id: int, data: dict) -> Optional[UserContacts]:
        async with async_session() as session:
            stmt = select(User).options(joinedload(User.contacts)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if not user:
                return None

            if user.contacts:
                for key, val in data.items():
                    setattr(user.contacts, key, val)
            else:
                user.contacts = UserContacts(**data)

            await session.commit()
            return user.contacts
        
    @classmethod
    async def update_steam_profile(cls, user_id: int, data: dict) -> Optional[SteamProfile]:
        async with async_session() as session:
            stmt = select(User).options(joinedload(User.contacts)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if not user:
                return None
            
            if user.steam_profile:
                for key, val in data.items():
                    setattr(user.steam_profile, key, val)
            else:
                user.steam_profile = SteamProfile(**data)
            
    
    # @classmethod
    # async def update_integro(cls, user_id: int, data: dict) -> Optional[UserIntegro]:
    #     async with async_session() as session:
    #         stmt = select(User).options(joinedload(User.integro)).where(User.id == user_id)
    #         result = await session.execute(stmt)
    #         user = result.scalars().first()
    #         if not user:
    #             return None

    #         if user.integro:
    #             for key, val in data.items():
    #                 setattr(user.contacts, key, val)
    #         else:
    #             user.integro = UserIntegro(**data)

    #         await session.commit()
    #         return user.integro

class UserInteractionDAO(BaseDAO[UserInteraction]):
    model = UserInteraction

    @classmethod
    async def get_all_user_interactions(cls, user_id: int) -> list[UserInteraction] | None:
        async with async_session() as session:
            query = select(cls.model).where(
                (cls.model.user_1_id == user_id) | 
                (cls.model.user_2_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def get_user_interactions(cls, user_id: int, game: str) -> list[UserInteraction] | None:
        async with async_session() as session:
            query = select(cls.model).where(
                (cls.model.user_1_id == user_id) | 
                (cls.model.user_2_id == user_id)
            ).filter(game=game)
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
        
class UserFollowDAO(BaseDAO[UserFollow]):
    model = UserFollow
    
    @classmethod
    async def follow(cls, follower_id: int, followed_id: int) -> UserFollow:
        return await cls.create(follower_id=follower_id, followed_id=followed_id)
    
    @classmethod
    async def find_follows(cls, user_id: int) -> list[UserFollow]:
        async with async_session() as session:
            query = (
                select(cls.model).where(UserFollow.follower_id==user_id)
                .options(
                    joinedload(UserFollow.followed)
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
        
    @classmethod
    async def find_followers(cls, user_id: int) -> list[UserFollow]:
        async with async_session() as session:
            query = (
                select(cls.model).where(UserFollow.followed_id==user_id)
                .options(
                    joinedload(UserFollow.follower)
                )
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
    
    @classmethod
    async def check_follow(cls, follower_id: int, followed_id: int) -> UserFollow:
        async with async_session() as session:
            follow = await session.execute(
                select(cls.model).where(UserFollow.follower_id == follower_id,
                                        UserFollow.followed_id == followed_id)
                )
            follow = follow.scalars().first()
            
            if not follow:
                return None
            else:
                return follow
            
# class UserIntegroTableDAO(BaseDAO[UserIntegro]):
#     model = UserIntegro
    
#     @classmethod
#     async def get_integrations(cls, user_id: int) -> Optional[UserIntegro]:
#         async with async_session() as session:
#             query = (
#                 select(cls.model).where(UserIntegro.user_id == user_id)
#             )
#             result = await session.execute(query)
#             return result.scalars().one_or_none()
        