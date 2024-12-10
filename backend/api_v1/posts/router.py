from backend.api_v1.auth.auth import get_current_user
from backend.api_v1.posts.dao import PostDAO
from fastapi import APIRouter, Depends
from models_nosql import PostCreate, PostResponse

posts_router = APIRouter(prefix='/posts', tags=['Posts management'])


@posts_router.post('/posts/', response_model=PostResponse)
def create_new_post(post: PostCreate, current_user=Depends(get_current_user)):
    PostDAO.create(title=post.title, content=post.content, user_id=current_user.id)
    return {'gewgew': 'gwegweg'}


@posts_router.get('/posts/', response_model=list[PostResponse])
def read_posts(skip: int = 0, limit: int = 10):
    posts = PostDAO.get(skip, limit)
    return posts
