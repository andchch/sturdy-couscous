from datetime import datetime
from pydantic import BaseModel


class ContactsSchema(BaseModel):
    vk: str | None
    telegram: str | None
    steam: str | None
    discord: str | None
    
class ShortUser(BaseModel):
    id: int
    username: str
    avatar_url: str
    
class GetAllUsersResponse(BaseModel):
    users: list[ShortUser]
    
class UserInfoScheme(BaseModel):
    purpose: str | None
    self_assessment_lvl: str | None
    preferred_communication: str | None
    hours_per_week: int | None

class GetMeResponse(BaseModel):
    id: int
    email: str
    username: str
    registration_time: datetime
    gender: str | None
    dof: datetime | None
    avatar_url: str | None
    contacts: ContactsSchema | None
    info: UserInfoScheme | None
    
class GetUserResponse(BaseModel):
    id: int
    username: str
    gender: str | None
    dof: datetime | None
    contacts: ContactsSchema | None
    
class CreateUserResponse(BaseModel):
    status: bool
    info: str
    
class UpdateCurrentUserRequest(BaseModel):
    # gender: str
    purpose: str
    self_assessment_lvl: str
    preferred_communication: str
    hours_per_week: int


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    dob: datetime
    gender: str
    timezone: str
    
    
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
    
class OnlyStatusResponse(BaseModel):
    status: str
    
class GetAvatarResponse(BaseModel):
    avatar_url: str
    
class UsersShort(BaseModel):
    id: int
    username: str
    
class CommunityShort(BaseModel):
    id: int
    name: str
    
class GetFollowersResponse(BaseModel):
    users: list[UsersShort]

class GetFollowingsResponse(BaseModel):
    users: list[UsersShort]
    communities: list[CommunityShort]
    
class UpdateCreditsRequest(BaseModel):
    new_username: str | None
    new_password: str | None
    new_dob: datetime | None
    