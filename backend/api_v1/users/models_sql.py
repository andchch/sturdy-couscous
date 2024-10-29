from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api_v1.users.enums import GenderEnum, PurposeEnum, CommunicationTypeEnum, RatingEnum, SelfAssessmentLvlEnum, WeekdayEnum
from api_v1.games.enums import GenreEnum
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
    self_assessment_lvl: Mapped[SelfAssessmentLvlEnum]
    preferred_communication: Mapped[CommunicationTypeEnum]
    
    user: Mapped['User'] = relationship('User',
                                        back_populates='profile',
                                        uselist=False)
    platforms: Mapped[list[Platform]] = relationship(secondary=user_profile_platform_association_table)
    
    purpose_weight: Mapped[float] = mapped_column(default=0.1)
    self_assessment_lvl_weight: Mapped[float] = mapped_column(default=0.1)
    preferred_communication_weight: Mapped[float] = mapped_column(default=0.1)
    platforms_weight: Mapped[float] = mapped_column(default=0.1)
    playtime_weight: Mapped[float] = mapped_column(default=0.1)
    
    hours_per_week_weight: Mapped[int| None]
    preferred_days_weight: Mapped[WeekdayEnum| None]
    preferred_genres: Mapped[GenreEnum| None] = mapped_column(default=0.1)
    
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
    