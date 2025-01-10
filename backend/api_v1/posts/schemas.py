from datetime import datetime
from pydantic import BaseModel


class OnlyStatusResponse(BaseModel):
    status: str
    
class Author(BaseModel):
    id: int
    username: str
    
class Community(BaseModel):
    id: int
    name: str
    
class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: Author
    community: Community | None
    
class GetPostsResponse(BaseModel):
    posts: list[Post]
    