from backend.api_v1.communities.models_sql import Community
from backend.api_v1.posts.utilities import serialize_post_without_community
from backend.redis.cache import RedisController


def serialize_community_with_members(community: Community):
    return {
        'id': community.id,
        'name': community.name,
        'description': community.description,
        'creator_id': community.creator_id,
        'members': [
            {
                'id': member.id,
                'username': member.username,
            }
            for member in community.members
        ],
    }

async def serialize_full_community(community: Community, rediska: RedisController):
    ret = {
        'id': community.id,
        'name': community.name,
        'description': community.description,
        'creator_id': community.creator_id,
        'members': [
            {
                'id': member.id,
                'username': member.username,
            }
            for member in community.members
        ]
    }
    
    add = {'posts': [await serialize_post_without_community(post, rediska) for post in community.posts]}
    ret.update(add)
    
    return ret
