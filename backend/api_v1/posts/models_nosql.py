from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class MediaFile(BaseModel):
    file_url: str
    file_type: str

class GetPostsResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    media_files: list[MediaFile]
