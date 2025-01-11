from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.communities.dao import CommunityMembershipDAO
from backend.api_v1.feed.schemas import GetFeed
from backend.api_v1.users.dao import UserFollowDAO
from backend.api_v1.posts.dao import PostDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User


from fastapi import Query

from backend.api_v1.posts.utilities import serialize_post
from backend.redis.cache import RedisController, get_redis_controller

feed_router = APIRouter(prefix='/feed', tags=['Feed'])

@feed_router.get('/', response_model=GetFeed)
async def get_feed(
    rediska: Annotated[RedisController, Depends(get_redis_controller)],
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),  # Ограничение на 50 постов за раз
    offset: int = Query(0, ge=0)
):
    """Получить ленту новостей (посты подписанных пользователей и групп)"""
    following_ids = []
    following = await UserFollowDAO.find_all(follower_id=current_user.id)
    
    for obj in following:
        following_ids.append(obj.followed_id)

    communities = await CommunityMembershipDAO.get_all_users_communities(current_user.id)
    community_ids = []
    
    for obj in communities:
        community_ids.append(obj.community_id)

    feed = await PostDAO.get_users_feed(following_ids, community_ids, limit, offset)

    return {
        'posts': [await serialize_post(post, rediska) for post in feed]
    }
