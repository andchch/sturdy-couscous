from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from backend.api_v1.external_integration.models_sql import SteamProfile
from backend.core.dao import BaseDAO
from backend.api_v1.users.models_sql import User, UserContact, UserFollow, UserInfo, UserWeight#, UserInteraction
from backend.core.database_sql import async_session

class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_by_email(cls, email: str) -> Optional[User]:
        async with async_session() as session:
            query = ( 
                select(cls.model)
                .where(cls.model.email == email)
                .options(
                    joinedload(User.contacts),
                    joinedload(User.info)
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
                .options(joinedload(cls.model.contacts))
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get_by_id_with_rs_info(cls, model_id):
        async with async_session() as session:
            query = (
                select(cls.model).where(cls.model.id == model_id)
                .options(joinedload(cls.model.info))
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def get_others(cls, model_id):
        async with async_session() as session:
            query = (
                select(cls.model).where(cls.model.id != model_id)
                .options(joinedload(cls.model.info))
            )
            result = await session.execute(query)
            return result.unique().scalars()

        
    @classmethod
    async def update_contacts(cls, user_id: int, data: dict) -> Optional[UserContact]:
        async with async_session() as session:
            stmt = select(cls.model).options(joinedload(User.contacts)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if not user:
                return None

            if user.contacts:
                for key, val in data.items():
                    setattr(user.contacts, key, val)
            else:
                user.contacts = UserContact(**data)

            await session.commit()
            return user.contacts
        
    @classmethod
    async def update_steam_profile(cls, user_id: int, data: dict) -> Optional[SteamProfile]:
        async with async_session() as session:
            stmt = select(cls.model).options(joinedload(User.steam_profile)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if not user:
                return None
            
            if user.steam_profile:
                for key, val in data.items():
                    setattr(user.steam_profile, key, val)
            else:
                user.steam_profile = SteamProfile(**data)
            await session.commit()
            return user.steam_profile
        
    @classmethod
    async def update_user_info(cls, user_id: int, data: dict) -> Optional[UserInfo]:
        async with async_session() as session:
            stmt = select(cls.model).options(joinedload(User.info)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return None
            
            if user.info:
                for key, val in data.items():
                    print(f'{key} {val}')
                    setattr(user.info, key, val)
            else:
                user.info = UserInfo(**data)
                
            await session.commit()
            return user.info
     
    @classmethod   
    async def update_weights(cls, user_id: int, data: dict):
        async with async_session() as session:
            stmt = select(cls.model).options(joinedload(User.weights)).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return None
            
            if user.weights:
                for key, val in data.items():
                    setattr(user.weights, key, val)
            else:
                user.weights = UserWeight(**data)
            await session.commit()
            return user.weights

# class UserInteractionDAO(BaseDAO[UserInteraction]):
#     model = UserInteraction
#
#     @classmethod
#     async def get_all_user_interactions(cls, user_id: int) -> list[UserInteraction] | None:
#         async with async_session() as session:
#             query = select(cls.model).where(
#                 (cls.model.user_1_id == user_id) |
#                 (cls.model.user_2_id == user_id)
#             )
#             result = await session.execute(query)
#             return result.scalars().all()
#
#     @classmethod
#     async def get_user_interactions(cls, user_id: int, game: str) -> list[UserInteraction] | None:
#         async with async_session() as session:
#             query = select(cls.model).where(
#                 (cls.model.user_1_id == user_id) |
#                 (cls.model.user_2_id == user_id)
#             ).filter(game=game)
#             result = await session.execute(query)
#             return result.scalars().all()
#
#     @classmethod
#     async def create_interaction(
#         cls,
#         user_1_id: int,
#         user_2_id: int,
#         game: str,
#         user_1_rating: int,
#         user_2_rating: int
#     ) -> UserInteraction:
#         return await cls.create(
#             user_1_id=user_1_id,
#             user_2_id=user_2_id,
#             game=game,
#             user_1_rating=user_1_rating,
#             user_2_rating=user_2_rating
#         )
        
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
            
    @classmethod
    async def unfollow(cls, follower_id: int, followed_id: int):
        async with async_session() as session:
            await session.execute(
                delete(cls.model).where(
                    cls.model.follower_id == follower_id,
                    cls.model.followed_id == followed_id
                    )
                )
            await session.commit()

class UserWeightsDAO(BaseDAO[UserFollow]):
    model = UserWeight
    
    @classmethod
    async def get_by_user_id(cls, user_id: int) -> UserWeight:
        async with async_session() as session:
            query = (
                select(cls.model).where(cls.model.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def create_default(cls, user_id: int) -> UserWeight:
        weights = UserWeight(user_id=user_id, purpose_weight=0.25,
                             self_assessment_lvl_weight=0.25,
                             preferred_communication_weight=0.25,
                             hours_per_week_weight=0.25)
        await UserDAO.update(user_id, weights=weights)
        return weights
    