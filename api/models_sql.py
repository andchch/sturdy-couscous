from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr, mapped_column
from typing import Annotated
from sqlalchemy import func
from datetime import datetime
# from database import Base

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        tablename = ''
        modified_string = list(
            map(lambda x: '_' + x if x.isupper() else x, self.__name__)
        )
        split_string = ''.join(modified_string).split('_')
        split_string = list(filter(lambda x: x != '', split_string))
        for word in split_string:
            tablename += word + '_'
        return f'{tablename[:-1].lower()}s'

    # TODO: Check if pydantic warnings are caused here
    created_at: datetime = Annotated[
        datetime, mapped_column(server_default=func.now())
    ]
    updated_at: datetime = Annotated[
        datetime,
        mapped_column(server_default=func.now(), onupdate=datetime.now),
    ]

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    gender = Column(String(10))
    age = Column(Integer)
    language = Column(String)
    time_zone = Column(String)

    profile = relationship('UserProfile', back_populates='user', uselist=False)


class UserProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    self_assessment_level = Column(String)
    motivation = Column(String)
    preferred_communication = Column(String)
    typical_play_time = Column(String)
    weekly_play_hours = Column(Integer)
    preferred_play_days = Column(String)

    user = relationship('User', back_populates='profile')


class PreferredGenre(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    genre = Column(String)


class Platform(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class UserPlatform(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
