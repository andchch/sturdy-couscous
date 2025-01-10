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
        media = {
            "media_files": [{"file_url": post.media_files.file_url,
                                "file_type": post.media_files.file_type}]
            }
        ret.update(media)
    return ret


def serialize_post_without_community(post):
    ret = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,
        "author": {"id": post.author.id, "username": post.author.username},
    }
    if post.media_files:
        media = {
            "media_files": [{"file_url": post.media_files.file_url,
                             "file_type": post.media_files.file_type}]
            }
        ret.update(media)
    return ret
