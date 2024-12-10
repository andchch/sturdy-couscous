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
                    joinedload(Post.media_files)
                    )
                .offset(offset)
                .limit(limit)
            )
            result = await session.execute(query)
            return result.unique().scalars().all()


class MediaDAO(BaseDAO[Media]):
    model = Media
    