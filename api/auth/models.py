from sqlmodel import Field

from api.database import Base


class TokenBase(Base):
    id: int = Field(int, primary_key=True)
    token: str


class TokenBlacklist(TokenBase, table=True):
    pass
