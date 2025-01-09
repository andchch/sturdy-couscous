from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from backend.api_v1.posts.models_sql import Media, Post
from backend.core.dao import BaseDAO
from backend.core.database_sql import async_session


class PostDAO(BaseDAO[Post]):
    model = Post
    
    @classmethod
    async def get(cls, offset, limit) -> list[Post]:
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(
                    joinedload(Post.author),
                    joinedload(Post.media_files),
                    joinedload(Post.community)
                    )
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
        
    @classmethod
    async def get_by_user_id(cls, user_id) -> list[Post]:
        async with async_session() as session:
            query = (
                select(cls.model)
                .options(
                    joinedload(Post.author),
                    joinedload(Post.media_files),
                    joinedload(Post.community)
                    )
            .filter_by(user_id=user_id)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
        
    @classmethod
    async def get_users_feed_from_users(cls, following_ids, limit, offset):
        async with async_session() as session:
            last_30_days = datetime.now() - timedelta(days=30)
            query = (
                select(cls.model)
                .where(Post.user_id.in_(following_ids), Post.created_at >= last_30_days)
                .options(joinedload(Post.author),
                         joinedload(Post.media_files),
                         joinedload(Post.community))
                .order_by(Post.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
        
    @classmethod
    async def get_users_feed_from_communities(cls, community_ids, limit, offset):
        async with async_session() as session:
            last_30_days = datetime.now() - timedelta(days=30)
            query = (
                select(cls.model)
                .where(Post.community_id.in_(community_ids), Post.created_at >= last_30_days)
                .options(joinedload(Post.author),
                         joinedload(Post.media_files),
                         joinedload(Post.community))
                .order_by(Post.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()


class MediaDAO(BaseDAO[Media]):
    model = Media
    