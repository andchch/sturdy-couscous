from datetime import datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship
from backend.core.database_sql import Base, unique_str, idx_str
import enum


class GenderEnum(enum.StrEnum):
    MALE = 'мужской'
    FEMALE = 'женский'
    
class PurposeEnum(enum.StrEnum):
    FUN = 'Для развлечения'
    RESULT = 'На результат'
    
class SelfAssLvl(enum.StrEnum):
    LOW = 'Начинающий'
    MID = 'Средний'
    HIGH = 'Продвинутый'
    
class CommunicationType(enum.StrEnum):
    VOICE = 'Голосовой'
    TEXT = 'Внутриигровой чат'
    NO = 'Нет'
    
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
    gender: Mapped[GenderEnum]
    dof: Mapped[datetime]
    timezone: Mapped[str]
    
    profile: Mapped['UserProfile'] = relationship('UserProfile',
                                                  back_populates='user',
                                                  uselist=False,
                                                  lazy='joined')
    
class UserProfile(Base):
    purpose: Mapped[PurposeEnum]
    self_ass_lvl: Mapped[SelfAssLvl]
    preferred_communication: Mapped[CommunicationType]
    
    
    user: Mapped['User'] = relationship('User',
                                        back_populates='profile',
                                        uselist=False)
    platforms: Mapped[list[Platform]] = relationship(secondary=user_profile_platform_association_table)
    