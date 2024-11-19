from datetime import datetime
from sqlalchemy import Column, ForeignKey, LargeBinary, String, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.api_v1.users.enums import GenderEnum, PurposeEnum, CommunicationTypeEnum, RatingEnum, SelfAssessmentLvlEnum, PlatformEnum
from backend.api_v1.games.enums import GenreEnum
from backend.core.database_sql import Base, unique_str, idx_str, not_null_str, weight_str
# from api_v1.users.enums import GenderEnum, PurposeEnum, CommunicationTypeEnum, RatingEnum, SelfAssessmentLvlEnum, PlatformEnum
# from api_v1.games.enums import GenreEnum
# from core.database_sql import Base, unique_str, idx_str, not_null_str, weight_str


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

class User(Base):
    username: Mapped[unique_str]
    email: Mapped[idx_str]
    hashed_password: Mapped[str]
    gender: Mapped[GenderEnum | None]
    dof: Mapped[datetime | None]
    timezone: Mapped[str | None]
    avatar = Column(LargeBinary)
    content_type = Column(String)
    
    purpose: Mapped[PurposeEnum | None]
    self_assessment_lvl: Mapped[SelfAssessmentLvlEnum | None]
    preferred_communication: Mapped[CommunicationTypeEnum | None]
    hours_per_week: Mapped[int | None]
    
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
    
    preferred_genres: Mapped[list[Genre]] = relationship(secondary=user_genre_association_table)
    preferred_platforms: Mapped[list[Platform]] = relationship(secondary=user_platform_association_table)
    
    interactions_as_user_1: Mapped[list['UserInteraction']] = relationship(back_populates='user_1',
                                                                            foreign_keys='UserInteraction.user_1_id')
    interactions_as_user_1: Mapped[list['UserInteraction']] = relationship(back_populates='user_2',
                                                                            foreign_keys='UserInteraction.user_2_id')
    
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
    