from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.communities.dao import CommunityDAO, CommunityMembershipDAO
from backend.api_v1.communities.models_sql import Community
from backend.api_v1.communities.schemes import CommunityCreate, CommunityCreateResponse, CommunityJoinResponse, CommunityListResponse, EditCommunity
from backend.api_v1.communities.utilities import serialize_community_with_members
from backend.api_v1.users.dao import UserFollowDAO
from backend.api_v1.posts.dao import PostDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User, UserFollow


from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

feed_router = APIRouter(prefix="/feed", tags=["Feed"])

@feed_router.get("/")
async def get_feed(
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),  # Ограничение на 50 постов за раз
    offset: int = Query(0, ge=0)
):
    """Получить ленту новостей (посты подписанных пользователей и групп)"""
    following_ids = []
    following = await UserFollowDAO.find_all(follower_id=current_user.id)
    
    for obj in following:
        following_ids.append(obj.followed_id)
    print(following_ids)

    # 🔹 2. Получаем ID групп, в которых состоит пользователь
    communities = await CommunityMembershipDAO.get_all_users_communities(current_user.id)
    community_ids = []
    
    for obj in communities:
        community_ids.append(obj.community_id)

    # 🔹 3. Получаем посты подписанных пользователей
    user_posts = await PostDAO.get_users_feed_from_users(following_ids, limit, offset)

    # 🔹 4. Получаем посты из групп
    group_posts = await PostDAO.get_users_feed_from_communities(community_ids, limit, offset)

    # 🔹 5. Форматируем ответ
    def serialize_post(post):
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "author": {"id": post.author.id, "username": post.author.username},
            "media_files": [{"file_url": media.file_url, "file_type": media.file_type} for media in post.media_files or []],
            "community": {"id": post.community.id, "name": post.community.name} if post.community else None
        }

    return {
        "user_posts": [serialize_post(post) for post in user_posts],
        "group_posts": [serialize_post(post) for post in group_posts]
    }
