from pydantic import BaseModel

from backend.api_v1.posts.schemas import Post


class CommunityCreate(BaseModel):
    name: str
    description: str
    
class CommunityCreateResponse(BaseModel):
    id: int
    name: str
    
class CommunityMessageResponse(BaseModel):
    message: str

class EditCommunity(BaseModel):
    name: str
    description: str
        
class Member(BaseModel):
    id: int
    username: str
    
class CommunityListResponse(BaseModel):
    id: int
    name: str
    description: str
    creator_id: int
    members: list[Member] | None
    
class GetCommunityResponse(CommunityListResponse):
    posts: list[Post]
    
class GetCommunity(BaseModel):
    id: int
    name: str
    description: str
    creator_id: int
    members: list[Member] | None
    posts: list[Post]
    