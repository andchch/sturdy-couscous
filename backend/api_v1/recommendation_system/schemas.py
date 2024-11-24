from pydantic import BaseModel


class data(BaseModel):
    username: str
    score: float


class finderResponse(BaseModel):
    list[dict[data]]
    