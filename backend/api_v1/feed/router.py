from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.communities.dao import CommunityDAO, CommunityMembershipDAO
from backend.api_v1.communities.models_sql import Community
from backend.api_v1.communities.schemes import CommunityCreate, CommunityCreateResponse, CommunityMessageResponse, CommunityListResponse, EditCommunity
from backend.api_v1.communities.utilities import serialize_community_with_members
from backend.api_v1.feed.schemas import GetFeed
from backend.api_v1.users.dao import UserFollowDAO
from backend.api_v1.posts.dao import PostDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User, UserFollow


from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.utilities import serialize_post

feed_router = APIRouter(prefix="/feed", tags=["Feed"])

@feed_router.get("/", response_model=GetFeed)
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

    # 🔹 2. Получаем ID групп, в которых состоит пользователь
    communities = await CommunityMembershipDAO.get_all_users_communities(current_user.id)
    community_ids = []
    
    for obj in communities:
        community_ids.append(obj.community_id)

    feed = await PostDAO.get_users_feed(following_ids, community_ids, limit, offset)

    return {
        "posts": [serialize_post(post) for post in feed]
    }
