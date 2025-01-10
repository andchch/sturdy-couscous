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
    return {
        'posts': [serialize_post(post) for post in posts]
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
    

@posts_router.get('/load_users')#, response_model=list[GetPostsResponse])
async def get_users_posts(id: int):
    posts = await PostDAO.get_by_user_id(id)
    
    return {
        'posts': [serialize_post(post) for post in posts]
    }
