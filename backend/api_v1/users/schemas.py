from pydantic import BaseModel


class GetMeResponse(BaseModel):
    username: str
    email: str
    gender: str | None
    date_of_birth: str | None
    
class CreateUserResponse(BaseModel):
    status: str
    
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
    hours_per_week: int
    preferred_communication: str
    purpose: str
    self_assessment_lvl: str

class RSResponse(BaseModel):
    result: list[GetMeResponse]


class UpdateCredentialsRequest(BaseModel):
    username: str | None
    