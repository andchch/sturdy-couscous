from sqlalchemy.orm import Mapped

from backend.core.database_sql import Base, unique_str, idx_str, not_null_str, weight_str


class Game(Base):
    steamid: Mapped[idx_str]
    appid: Mapped[int]
    name: Mapped[str]
    playtime_hours: Mapped[float]

class Achievement(Base):
    steamid: Mapped[idx_str]
    appid: Mapped[int]
    achievement = Mapped[str]
    unlocked = Mapped[bool]
    