from pydantic import BaseModel


class CommunityCreate(BaseModel):
    name: str
    description: str
    
class CommunityCreateResponse(BaseModel):
    id: int
    name: str
    
class CommunityJoinResponse(BaseModel):
    message: str
    
class Member(BaseModel):
    id: int
    username: str
    
class CommunityListResponse(BaseModel):
    id: int
    name: str
    description: str
    members: list[Member] | None
    
class EditCommunity(BaseModel):
    name: str
    description: str
    