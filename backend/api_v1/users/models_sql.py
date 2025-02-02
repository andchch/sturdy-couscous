from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api_v1.posts.models_sql import Post
from backend.api_v1.users.enums import RatingEnum, PlatformEnum
from backend.api_v1.games.enums import GenreEnum
from backend.core.database_sql import Base, unique_str, idx_str, not_null_str, weight_str


user_platform_association_table = Table(
    'user_platform_association',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('platform_id', ForeignKey('platforms.id'), nullable=False))

user_genre_association_table = Table(
    'user_genre_association',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('genre_id', ForeignKey('genres.id'), nullable=False))

class Genre(Base):
    name: Mapped[GenreEnum]

class Platform(Base):
    name: Mapped[PlatformEnum]
    
class UserFollow(Base):
    id = None
    follower_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    follower: Mapped['User'] = relationship('User', foreign_keys=[follower_id], back_populates='following')
    followed: Mapped['User'] = relationship('User', foreign_keys=[followed_id], back_populates='followers')

    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='uq_user_follow'),)
    
class UserContacts(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    vk: Mapped[str | None]
    telegram: Mapped[str | None]
    steam: Mapped[str | None]
    discord: Mapped[str | None]
    
    user: Mapped['User'] = relationship('User', back_populates='contacts')
    
class UserWeights(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    # --- Weights ---
    purpose_weight: Mapped[weight_str]
    self_assessment_lvl_weight: Mapped[weight_str]
    preferred_communication_weight: Mapped[weight_str]
    preferred_platforms_weight: Mapped[weight_str]
    # ---- NoSQL ----
    playtime_weight: Mapped[weight_str]
    hours_per_week_weight: Mapped[weight_str]
    preferred_days_weight: Mapped[weight_str]
    preferred_genres_weight: Mapped[weight_str]
    # --- Weights ---
    
    user: Mapped['User'] = relationship('User', back_populates='weights')
    
class UserInfo(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    
    # purpose: Mapped[PurposeEnum | None]
    # self_assessment_lvl: Mapped[SelfAssessmentLvlEnum | None]
    # preferred_communication: Mapped[CommunicationTypeEnum | None]
    purpose: Mapped[str | None]
    self_assessment_lvl: Mapped[str | None]
    preferred_communication: Mapped[str | None]
    
    hours_per_week: Mapped[int | None]
    
    user: Mapped['User'] = relationship('User', back_populates='info')
    
class User(Base):
    username: Mapped[unique_str]
    email: Mapped[idx_str]
    hashed_password: Mapped[str]
    
    # gender: Mapped[GenderEnum | None]
    gender: Mapped[str | None]
    
    dof: Mapped[datetime | None]
    avatar_url: Mapped[str | None]
    
    steam_profile: Mapped['SteamProfile'] = relationship(
        'SteamProfile', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    
    contacts: Mapped['UserContacts'] = relationship(
        'UserContacts', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    
    weights: Mapped['UserWeights'] = relationship(
        'UserWeights', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    
    info: Mapped['UserInfo'] = relationship(
        'UserInfo', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    
    following: Mapped[list['UserFollow']] = relationship(
        'UserFollow', foreign_keys=[UserFollow.follower_id], back_populates='follower', cascade='all, delete-orphan'
    )
    
    followers: Mapped[list['UserFollow']] = relationship(
        'UserFollow', foreign_keys=[UserFollow.followed_id], back_populates='followed', cascade='all, delete-orphan'
    )
    
    preferred_genres: Mapped[list[Genre]] = relationship(secondary=user_genre_association_table)
    preferred_platforms: Mapped[list[Platform]] = relationship(secondary=user_platform_association_table)
    
    interactions_as_user_1: Mapped[list['UserInteraction']] = relationship(back_populates='user_1',
                                                                            foreign_keys='UserInteraction.user_1_id')
    interactions_as_user_2: Mapped[list['UserInteraction']] = relationship(back_populates='user_2',
                                                                            foreign_keys='UserInteraction.user_2_id')
    
    posts: Mapped[list['Post']] = relationship(
        'Post', back_populates='author', cascade='all, delete-orphan'
    )
    
    communities: Mapped[list['Community']] = relationship(
        'Community',
        secondary='community_memberships',
        back_populates='members',
    )
    
class UserInteraction(Base):
    user_1_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user_2_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    game: Mapped[not_null_str]
    user_1_rating: Mapped[RatingEnum]
    user_2_rating: Mapped[RatingEnum]
    
    user_1: Mapped['User'] = relationship(back_populates='interactions_as_user_1',
                                                 foreign_keys=[user_1_id])
    user_2: Mapped['User'] = relationship(back_populates='interactions_as_user_1',
                                                 foreign_keys=[user_2_id])
    