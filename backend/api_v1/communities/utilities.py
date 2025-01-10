from backend.api_v1.communities.models_sql import Community


def serialize_community_with_members(community: Community):
    return {
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "creator": community.creator_id,
        "members": [
            {
                "id": member.id,
                "username": member.username,
            }
            for member in community.members
        ],
    }
    
def serialize_post(post):
        ret = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "author": {"id": post.author.id, "username": post.author.username},
            "community": {"id": post.community.id, "name": post.community.name} if post.community else None
        }
        if post.media_files:
            add = {
                "media_files": [{"file_url": post.media_files.file_url,
                                 "file_type": post.media_files.file_type}]
                }
            ret.update(add)
        return ret

def serialize_full_community(community: Community):
    print(vars(community))
    print(vars(community.posts))
    ret = {
        "id": community.id,
        "name": community.name,
        "description": community.description,
        "creator": community.creator_id,
        "members": [
            {
                "id": member.id,
                "username": member.username,
            }
            for member in community.members
        ]
    }
    
    add = {'posts': [serialize_post(post) for post in community.posts]}
    ret.update(add)
    
    return ret
