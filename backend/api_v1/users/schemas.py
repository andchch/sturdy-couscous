from datetime import datetime
from zoneinfo import available_timezones
from typing import List, Optional, Dict
from pydantic import BaseModel, field_validator

from backend.api_v1.users.enums import GenderEnum, PurposeEnum, RatingEnum


class StatusResponse(BaseModel):
    status: bool
    info: str


class ContactsSchema(BaseModel):
    telegram: str | None
    steam: str | None
    discord: str | None

    
class UserInfoScheme(BaseModel):
    purpose: str | None
    preferred_communication: str | None


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
    description: str


class GetUserResponse(BaseModel):
    id: int
    username: str
    gender: str | None
    dob: datetime | None
    contacts: ContactsSchema | None
    description: str | None


class UpdateCurrentUserRequest(BaseModel):
    gender: GenderEnum | None


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    dob: datetime
    gender: GenderEnum
    timezone: str

    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v):
        if v not in available_timezones():
            raise ValueError('Invalid timezone')
        return v


class GetTimezonesResponse(BaseModel):
    timezones: list[str]


class UpdateContactsRequest(BaseModel):
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
    new_dob: datetime | None
    new_bio: str | None


class UpdateDescriptionsRequest(BaseModel):
    description: str


class CreateSurveyRequest(BaseModel):
    genres: list[str]
    purpose: str
    preferred_communication: str
    preferred_days: str
    preferred_time: str
    favorite_games: list[str]
    
    
class ChangePasswordRequest(BaseModel):
    new_password: str


# Рекомендации
class RecommendationResponse(BaseModel):
    user: Dict[str, str]
    compatibility_score: float
    matching_factors: List[str]
    rating: Dict[str, float | int | Dict[str, int]]
    recent_ratings: List[Dict[str, str | float | datetime]]

class TopRatedRecommendationResponse(BaseModel):
    user: Dict[str, str]
    compatibility_score: float
    matching_factors: List[str]
    rating: Dict[str, float | int | Dict[str, int]]

class RecommendationSummaryResponse(BaseModel):
    user: Dict[str, str]
    recommendations: List[Dict[str, str | float | List[str]]]
    rating_summary: Dict
    top_rated_users: List[Dict[str, str | float]]

# Оценки
class RatingRequest(BaseModel):
    rating: RatingEnum
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    rating: str
    comment: Optional[str]
    from_user: str
    date: datetime

class RatingStatsResponse(BaseModel):
    average_rating: float
    total_ratings: int
    rating_distribution: Dict[str, int]

class RatingTrendResponse(BaseModel):
    trend: Dict[str, float]

class RatingImpactResponse(BaseModel):
    average_rating: float
    rating_count: int
    rating_strength: float
    recommendation_boost: float

class TopRatedUserResponse(BaseModel):
    user: Dict[str, str]
    rating: float

class UsersShort(BaseModel):
    id: int
    username: str
    
class GetFollowingsResponse(BaseModel):
    users: list[UsersShort]
    
class ShortUser(BaseModel):
    id: int
    username: str
    avatar_url: str
    
class GetAllUsersResponse(BaseModel):
    users: list[ShortUser]