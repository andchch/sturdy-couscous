from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.core.database_sql import Base, unique_str


class SteamProfile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    steam_id: Mapped[unique_str]
    steam_name: Mapped[str]
    steam_avatar: Mapped[str]
    profile_url: Mapped[str]

    user: Mapped['User'] = relationship('User', back_populates='steam_profile')
    