from pydantic import BaseModel

from games.models_nosql import GameModel
from games.enums import Weekdays, Genres


class UserGamesModel(BaseModel):
    user_id: str
    games: list[GameModel]
    
class PlaytimeModel(BaseModel):
    morning: bool
    afternoon: bool
    evening: bool
    night: bool
    
class UserPreferencesModel(BaseModel):
    user_id: str
    playtime: PlaytimeModel
    hours_per_week: int
    preferred_days: list[Weekdays]
    preferred_genres: list[Genres]
    