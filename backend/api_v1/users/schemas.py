from pydantic import BaseModel


class GetUserResponse(BaseModel):
    username: str
    email: str
    gender: str | None
    date_of_birth: str | None
    