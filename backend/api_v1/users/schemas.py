from datetime import datetime
from pydantic import BaseModel


class GetMeResponse(BaseModel):
    pass
    
class CreateUserResponse(BaseModel):
    status: str
    description: str
    
# class UpdateCurrentUserRequest(BaseModel):
#     purpose: str
#     self_assessment_lvl: str
#     preferred_communication: str
#     hours_per_week: int


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    
    
class UpdateMeRequest(BaseModel):
    gender: str | None
    
    purpose: str | None
    self_assessment_lvl: str | None
    preferred_communication: str | None
    hours_per_week: int | None
    

class RSResponse(BaseModel):
    result: list[GetMeResponse]


class UpdateCredentialsRequest(BaseModel):
    username: str | None
    
class UpdateMeContactsRequest(BaseModel):
    vk: str
    telegram: str
    steam: str
    discord: str
    
