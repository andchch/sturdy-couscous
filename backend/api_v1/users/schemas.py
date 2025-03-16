from datetime import datetime
from pydantic import BaseModel

from backend.api_v1.users.enums import GenderEnum, PurposeEnum, CommunicationTypeEnum


class StatusResponse(BaseModel):
    status: bool
    info: str


class ContactsSchema(BaseModel):
    vk: str | None
    telegram: str | None
    steam: str | None
    discord: str | None

    
class UserInfoScheme(BaseModel):
    purpose: PurposeEnum | None
    preferred_communication: str | None
    hours_per_week: int | None


class GetMeResponse(BaseModel):
    id: int
    email: str
    username: str
    registration_time: datetime
    gender: str
    dob: datetime
    avatar_url: str
    contacts: ContactsSchema | None
    info: UserInfoScheme | None


class GetUserResponse(BaseModel):
    id: int
    username: str
    gender: str | None
    dof: datetime | None
    contacts: ContactsSchema | None


class UpdateCurrentUserRequest(BaseModel):
    gender: GenderEnum | None
    purpose: PurposeEnum | None
    preferred_communication: CommunicationTypeEnum | None
    hours_per_week: int | None


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    dob: datetime
    gender: GenderEnum
    timezone: str


class UpdateContactsRequest(BaseModel):
    vk: str | None
    telegram: str | None
    steam: str | None
    discord: str | None


class OnlyStatusResponse(BaseModel):
    status: str


class GetAvatarResponse(BaseModel):
    avatar_url: str


class UsersShort(BaseModel):
    id: int
    username: str

    
class GetFollowersResponse(BaseModel):
    users: list[UsersShort]


class GetFollowingsResponse(BaseModel):
    users: list[UsersShort]


class UpdateCreditsRequest(BaseModel):
    new_username: str | None
    new_password: str | None
    new_dob: datetime | None


class UpdateDescriptionsRequest(BaseModel):
    description: str
