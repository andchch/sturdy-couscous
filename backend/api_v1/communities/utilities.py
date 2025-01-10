from backend.api_v1.communities.models_sql import Community
from backend.core.utilities import serialize_post, serialize_post_without_community


def serialize_community_with_members(community: Community):
    return {
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "creator_id": community.creator_id,
        "members": [
            {
                "id": member.id,
                "username": member.username,
            }
            for member in community.members
        ],
    }

def serialize_full_community(community: Community):
    ret = {
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "creator_id": community.creator_id,
        "members": [
            {
                "id": member.id,
                "username": member.username,
            }
            for member in community.members
        ]
    }
    
    add = {'posts': [serialize_post_without_community(post) for post in community.posts]}
    ret.update(add)
    
    return ret
