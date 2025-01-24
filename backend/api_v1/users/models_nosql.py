from pydantic import BaseModel

from .enums import WeekdayEnum


class PlaytimeModel(BaseModel):
    morning: bool
    afternoon: bool
    evening: bool
    night: bool
    
class UserPreferencesModel(BaseModel):
    user_id: int
    playtime: PlaytimeModel
    preferred_days: list[WeekdayEnum]
    