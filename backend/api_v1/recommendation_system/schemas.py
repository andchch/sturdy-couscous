from pydantic import BaseModel


class Mate(BaseModel):
    user_id: int
    username: str
    score: float

class finderResponse(BaseModel):
    info: str
    mates: list[Mate]
    