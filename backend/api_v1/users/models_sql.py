from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api_v1.users.enums import CommunicationTypeEnum, GenderEnum, PurposeEnum, PreferredDaysEnum, PreferredTimeEnum, RatingEnum
from backend.api_v1.games.enums import GenreEnum
from backend.core.database_sql import Base, unique_str, idx_str, weight
from backend.api_v1.external_integration.models_sql import SteamProfile

user_genre_association_table = Table(
    'user_genre_association',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('genre_id', ForeignKey('genres.id'), nullable=False))

class Genre(Base):
    name: Mapped[GenreEnum]

class UserFollow(Base):
    id = None
    follower_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    follower: Mapped['User'] = relationship('User', foreign_keys=[follower_id], back_populates='following')
    followed: Mapped['User'] = relationship('User', foreign_keys=[followed_id], back_populates='followers')

    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='uq_user_follow'),)
    
class UserContact(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    
    telegram: Mapped[str | None]
    steam: Mapped[str | None]
    discord: Mapped[str | None]
    
    user: Mapped['User'] = relationship('User', back_populates='contacts')
    
class UserWeight(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    purpose_weight: Mapped[weight]
    self_assessment_lvl_weight: Mapped[weight]
    preferred_communication_weight: Mapped[weight]
    preferred_platforms_weight: Mapped[weight]
    # ---- NoSQL ----
    playtime_weight: Mapped[weight]
    hours_per_week_weight: Mapped[weight]
    preferred_days_weight: Mapped[weight]
    preferred_genres_weight: Mapped[weight]
    
    user: Mapped['User'] = relationship('User', back_populates='weights')
    
class GamePlaytime(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    game_name: Mapped[str]
    playtime_hours: Mapped[float]
    
    user: Mapped['User'] = relationship('User', back_populates='game_playtimes')
    
    __table_args__ = (UniqueConstraint('user_id', 'game_name', name='uq_user_game_playtime'),)

class UserInfo(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    
    purpose: Mapped[str | None]
    preferred_communication: Mapped[str | None]
    preferred_days: Mapped[str | None]
    preferred_time: Mapped[str | None]
    
    user: Mapped['User'] = relationship('User', back_populates='info')
    
class UserRating(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    rater_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    rated_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    rating: Mapped[RatingEnum]
    comment: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    rater: Mapped['User'] = relationship('User', foreign_keys=[rater_id], back_populates='ratings_given')
    rated: Mapped['User'] = relationship('User', foreign_keys=[rated_id], back_populates='ratings_received')
    
    __table_args__ = (
        UniqueConstraint('rater_id', 'rated_id', name='uq_user_rating'),
    )

class User(Base):
    username: Mapped[unique_str]
    email: Mapped[idx_str]
    hashed_password: Mapped[str]
    
    gender: Mapped[GenderEnum | None]
    dob: Mapped[datetime | None]
    avatar_url: Mapped[str] = mapped_column(default='empty')
    description: Mapped[str | None]
    timezone: Mapped[str | None]
    
    preferred_genres: Mapped[list[Genre]] = relationship(
        secondary=user_genre_association_table
    )
    
    steam_profile: Mapped['SteamProfile'] = relationship(
        'SteamProfile', back_populates='user', uselist=False, 
        cascade='all, delete-orphan'
    )
    
    contacts: Mapped['UserContact'] = relationship(
        'UserContact', back_populates='user', uselist=False,
        cascade='all, delete-orphan'
    )
    
    weights: Mapped['UserWeight'] = relationship(
        'UserWeight', back_populates='user', uselist=False,
        cascade='all, delete-orphan'
    )
    
    info: Mapped['UserInfo'] = relationship(
        'UserInfo', back_populates='user', uselist=False, 
        cascade='all, delete-orphan'
    )
    
    following: Mapped[list['UserFollow']] = relationship(
        'UserFollow', foreign_keys=[UserFollow.follower_id], 
        back_populates='follower', cascade='all, delete-orphan'
    )
    
    followers: Mapped[list['UserFollow']] = relationship(
        'UserFollow', foreign_keys=[UserFollow.followed_id],
        back_populates='followed', cascade='all, delete-orphan'
    )
    
    game_playtimes: Mapped[list['GamePlaytime']] = relationship(
        'GamePlaytime', back_populates='user',
        cascade='all, delete-orphan'
    )
    
    ratings_given: Mapped[list['UserRating']] = relationship(
        'UserRating', foreign_keys=[UserRating.rater_id],
        back_populates='rater', cascade='all, delete-orphan'
    )
    
    ratings_received: Mapped[list['UserRating']] = relationship(
        'UserRating', foreign_keys=[UserRating.rated_id],
        back_populates='rated', cascade='all, delete-orphan'
    )
    

    