import datetime
import uuid
from sqlalchemy import UUID, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, index=True)
    name: Mapped[String]

    users = relationship('User', back_populates='role')


class User(BaseModel):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True, primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    username: Mapped[String] = mapped_column(String, index=True, unique=True, nullable=False)
    hashed_password: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    registration_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    role_id: Mapped[SmallInteger] = mapped_column(SmallInteger, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='users')

