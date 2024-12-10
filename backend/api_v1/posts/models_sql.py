from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.core.database_sql import Base
# from core.database_sql import Base

class Media(Base):
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    post = relationship("Post", back_populates='media_files')


class Post(Base):
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author: Mapped['User'] = relationship('User', back_populates='posts')
    media_files: Mapped['Media'] = relationship("Media", back_populates="post", cascade="all, delete-orphan")

    community_id: Mapped[int] = mapped_column(ForeignKey("communities.id"), nullable=True)
    community: Mapped['Community'] = relationship("Community", back_populates="posts")
    