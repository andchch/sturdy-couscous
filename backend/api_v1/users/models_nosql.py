from pydantic import BaseModel

from users.enums import WeekdayEnum
from games.models_nosql import GameModel


class UserGamesModel(BaseModel):
    user_id: int
    games: list[GameModel]
    
class PlaytimeModel(BaseModel):
    morning: bool
    afternoon: bool
    evening: bool
    night: bool
    
class UserPreferencesModel(BaseModel):
    user_id: int
    playtime: PlaytimeModel
    preferred_days: list[WeekdayEnum]
    