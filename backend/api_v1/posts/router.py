from typing import Optional
from backend.api_v1.posts.models_sql import Media
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.posts.dao import MediaDAO, PostDAO
from fastapi import APIRouter, Depends, File, Form, UploadFile
from backend.api_v1.posts.models_nosql import PostCreate, GetPostsResponse
from backend.core.database_s3 import upload_file_to_s3

posts_router = APIRouter(prefix='/posts', tags=['Posts management'])
S3_MEDIA_BUCKET='bucket-913415'


@posts_router.post('/create')
async def create_new_post(title: str = Form(...),
                          content: str = Form(...),
                          community_id: int = Form(None),
                          attachments: Optional[list[UploadFile]] = File(None),
                          current_user = Depends(get_current_user)):
    new_post = await PostDAO.create(title=title, content=content, user_id=current_user.id,
                                    community_id=community_id)
    
    if attachments is not None:
        for file in attachments:
            file_url = upload_file_to_s3(file, S3_MEDIA_BUCKET)
            await MediaDAO.create(file_url=file_url, file_type=file.content_type, post_id=new_post.id)
        
    return {'gewgew': 'gwegweg'}


@posts_router.get('/load')#, response_model=list[GetPostsResponse])
async def read_posts(skip: int = 0, limit: int = 10):
    posts = await PostDAO.get(skip, limit)
    ret = []
    for post in posts:
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
        if post.community is not None:
            community = {'community_name': post.community.name,
                         'community_id': post.community.id}
            post_json.update(community)
        ret.append(post_json)
    return ret

@posts_router.get('/load_users')#, response_model=list[GetPostsResponse])
async def get_users_posts(id: int):
    posts = await PostDAO.get_by_user_id(id)
    ret = []
    for post in posts:
        post_json = {'id': post.id,
                     'title': post.title,
                     'content': post.content,
                     'author_id': post.user_id,
                     'created_at': post.created_at
                     }
        # проверить
        if post.media_files is not None:
            media = {'media_files': [
                {'file_url': media.file_url, 'file_type': media.file_type} for media in post.media_files
                ]}
            post_json.update(media)
            
        ret.append(post_json)
    return ret
