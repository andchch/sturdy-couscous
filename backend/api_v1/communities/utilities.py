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

def serialize_full_community(community: Community):
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
    
    if community.posts is not None:
        posts = []
        for post in community.posts:
            post_json = {'id': post.id,
                        'title': post.title,
                        'content': post.content,
                        'author_id': post.user_id,
                        'created_at': post.created_at
            }
            if post.media_files is not None:
                media = {'media_files': [
                    {'file_url': media.file_url, 'file_type': media.file_type} for media in post.media_files
                    ]}
                post_json.update(media)
            posts.append(post_json)
        ret.update(posts)
    return ret