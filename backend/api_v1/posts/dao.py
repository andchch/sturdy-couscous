from sqlalchemy import select
from backend.api_v1.posts.models_sql import Post
from backend.core.dao import BaseDAO
from backend.core.database_sql import async_session


class PostDAO(BaseDAO[Post]):
    model = Post
    
    @classmethod
    async def get(cls, offset, limit) -> Post | None:
        async with async_session() as session:
            query = select(cls.model).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
