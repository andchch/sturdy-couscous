from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api_v1.users.users_enums import GenderEnum, PurposeEnum, CommunicationTypeEnum, RatingEnum, SelfAssLvlEnum
from core.database_sql import Base, unique_str, idx_str, not_null_str


user_profile_platform_association_table = Table(
    'user_profile_platforms_association',
    Base.metadata,
    Column('user_profile_id', ForeignKey('user_profiles.id'), nullable=False),
    Column('platform_id', ForeignKey('platforms.id'), nullable=False))


class Platform(Base):
    name: Mapped[str]

class User(Base):
    username: Mapped[unique_str]
    email: Mapped[idx_str]
    hashed_password: Mapped[str]
    gender: Mapped[GenderEnum| None]
    dof: Mapped[datetime| None]
    timezone: Mapped[str | None]
    
    profile: Mapped['UserProfile'] = relationship('UserProfile',
                                                  back_populates='user',
                                                  uselist=False,
                                                  lazy='joined')
    
class UserProfile(Base):
    purpose: Mapped[PurposeEnum]
    self_ass_lvl: Mapped[SelfAssLvlEnum]
    preferred_communication: Mapped[CommunicationTypeEnum]
    
    user: Mapped['User'] = relationship('User',
                                        back_populates='profile',
                                        uselist=False)
    platforms: Mapped[list[Platform]] = relationship(secondary=user_profile_platform_association_table)
    weights: Mapped['UserWeights'] = relationship('UserWeights',
                                                  back_populates='user_profile',
                                                  uselist=False,
                                                  lazy='joined')
    interactions_as_user_1: Mapped[list['UserInteraction']] = relationship(back_populates='user_1',
                                                                           foreign_keys='UserInteraction.user_1_id')
    interactions_as_user_2: Mapped[list['UserInteraction']] = relationship(back_populates='user_2',
                                                                           foreign_keys='UserInteraction.user_2_id')
    
class UserInteraction(Base):
    user_1_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user_2_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    game: Mapped[not_null_str]
    user_1_rating: Mapped[RatingEnum]
    user_2_rating: Mapped[RatingEnum]
    
    user_1: Mapped['UserProfile'] = relationship(back_populates='interaction_as_user_1',
                                                 foreign_keys=[user_1_id])
    user_2: Mapped['UserProfile'] = relationship(back_populates='interaction_as_user_2',
                                                 foreign_keys=[user_2_id])
    
class UserWeights(Base):
    user_profile: Mapped['User'] = relationship('UserProfile',
                                                back_populates='weights',
                                                uselist=False,
                                                lazy='joined')
    purpose_weight: Mapped[float]
    self_ass_lvl_weight: Mapped[float]
    preferred_communication_weight: Mapped[float]
    platforms_weight: Mapped[float]
    playtime_weight: Mapped[float]
    hours_per_week_weight: Mapped[float]
    preferred_days_weight: Mapped[float]
    preferred_genres: Mapped[float]
    