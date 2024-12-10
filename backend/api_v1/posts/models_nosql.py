from pydantic import BaseModel
from typing import Optional, List

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: str
    user_id: int

    class Config:
        orm_mode = True
