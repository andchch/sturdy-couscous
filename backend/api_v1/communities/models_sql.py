from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from backend.core.database_sql import Base

AltBase = declarative_base()

class CommunityMembership(Base):
    id = None
    __tablename__ = 'community_memberships'
     
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    community_id: Mapped[int] = mapped_column(ForeignKey('communities.id'), primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False, default='member')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.now)
    
class Community(Base):
    __tablename__ = 'communities'
    
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    members: Mapped[list['User']] = relationship(
        'User',
        secondary='community_memberships',
        back_populates='communities',
    )

    posts: Mapped[list['Post']] = relationship('Post', back_populates='community')
    