from backend.api_v1.communities.models_sql import Community


def serialize_community_with_members(community: Community):
    return {
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "members": [
            {
                "id": member.id,
                "username": member.username,
            }
            for member in community.members
        ],
    }
