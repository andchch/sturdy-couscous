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
    
class MediaFile(BaseModel):
    file_url: str
    file_type: str
    
class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: Author
    community: Community | None
    media_files: list[MediaFile]
    
class CommunityPost(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author: Author
    media_files: list[MediaFile]
    
class GetPostsResponse(BaseModel):
    posts: list[Post]
    
class GetCommunityPostsResponse(BaseModel):
    posts: list[CommunityPost] | None
    