from backend.core.database_s3 import get_cached_media_url
from backend.redis.cache import RedisController


async def serialize_post(post, rediska: RedisController):
    ret = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'author': {'id': post.author.id, 'username': post.author.username},
        'community': {'id': post.community.id, 'name': post.community.name} if post.community else None
    }
    if post.media_files:
        media = {
            'media_files': [{'file_url': await get_cached_media_url(post.media_files.file_url,
                                                              post.media_files.id,
                                                              rediska),
                             'file_type': post.media_files.file_type}]
            # 'media_files': [{'file_url': post.media_files.file_url,
            #                  'file_type': post.media_files.file_type}]
            }
        ret.update(media)
    else:
        add = {'media_files': []}
        ret.update(add)
    return ret


async def serialize_post_without_community(post, rediska: RedisController):
    ret = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'author': {'id': post.author.id, 'username': post.author.username},
        'community': None
    }
    if post.media_files:
        media = {
            'media_files': [{'file_url': await get_cached_media_url(post.media_files.file_url,
                                                              post.media_files.id,
                                                              rediska),
                             'file_type': post.media_files.file_type}]
            }
        ret.update(media)
    else:
        add = {'media_files': []}
        ret.update(add)
    return ret
