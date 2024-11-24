from pydantic import BaseModel


class GetTokenResponse(BaseModel):
    token: str
    token_type: str = 'bearer'
    