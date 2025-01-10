from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, union_all
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
        
    @classmethod
    async def get_users_feed(cls, following_ids: list[int], community_ids: list[int], limit: int, offset: int):
        async with async_session() as session:
            last_30_days = datetime.now() - timedelta(days=30)

            # Получаем ID постов + created_at (нужно для сортировки)
            users_query = select(Post.id, Post.created_at).where(Post.user_id.in_(following_ids), Post.created_at >= last_30_days)
            communities_query = select(Post.id, Post.created_at).where(Post.community_id.in_(community_ids), Post.created_at >= last_30_days)

            # Объединяем запросы
            union_query = union_all(users_query, communities_query).subquery()
            
            # Теперь сортируем по created_at и применяем limit/offset
            sorted_query = (
                select(union_query.c.id)  # Выбираем только ID
                .order_by(union_query.c.created_at.desc())
                .limit(limit)
                .offset(offset)
            )

            # Выполняем запрос (получаем ID постов)
            result = await session.execute(sorted_query)
            post_ids = [row[0] for row in result.all()]

            if not post_ids:
                return []

            # Теперь загружаем сами посты с подгруженными связями
            final_query = (
                select(Post)
                .where(Post.id.in_(post_ids))
                .options(
                    joinedload(Post.author),
                    joinedload(Post.media_files),
                    joinedload(Post.community)
                )
                .order_by(Post.created_at.desc())
            )

            final_result = await session.execute(final_query)
            return final_result.scalars().all()


class MediaDAO(BaseDAO[Media]):
    model = Media
    