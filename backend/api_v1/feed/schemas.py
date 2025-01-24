from pydantic import BaseModel

from backend.api_v1.posts.schemas import Post

class GetFeed(BaseModel):
    posts: list[Post]
