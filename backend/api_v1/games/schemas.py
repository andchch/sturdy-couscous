from pydantic import BaseModel


class SteamGame(BaseModel):
    appid: int
    name: str


class GetSteamGamesResponse(BaseModel):
    results: list[SteamGame]
