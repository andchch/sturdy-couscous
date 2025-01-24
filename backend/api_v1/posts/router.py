from typing import Annotated, Optional
from backend.api_v1.posts.schemas import OnlyStatusResponse, GetPostsResponse
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.posts.dao import MediaDAO, PostDAO
from fastapi import APIRouter, Depends, File, Form, UploadFile
from backend.core.database_s3 import upload_file_to_s3
from backend.api_v1.posts.utilities import serialize_post
from backend.redis.cache import RedisController, get_redis_controller

posts_router = APIRouter(prefix='/posts', tags=['Posts management'])
S3_MEDIA_BUCKET='bucket-913415'


@posts_router.post('/create', response_model=OnlyStatusResponse)
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
        
    return {'status': 'Пост успешно создан'}


@posts_router.get('/get-all-posts', response_model=GetPostsResponse)
async def read_posts(rediska: Annotated[RedisController, Depends(get_redis_controller)],
                     skip: int = 0, limit: int = 10):
    posts = await PostDAO.get(skip, limit)
    return {
        'posts': [await serialize_post(post, rediska) for post in posts]
    }

@posts_router.get('/{user_id}/get-posts', response_model=GetPostsResponse)
async def get_users_posts(user_id: int,
                          rediska: Annotated[RedisController, Depends(get_redis_controller)]):
    posts = await PostDAO.get_by_user_id(user_id)
    
    return {
        'posts': [await serialize_post(post, rediska) for post in posts]
    }
    
@posts_router.delete('/delete')
async def remove_post(post_id: int):
    await PostDAO.delete(post_id)
