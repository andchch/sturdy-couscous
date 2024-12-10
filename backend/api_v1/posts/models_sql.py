from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from backend.core.database_sql import Base
# from core.database_sql import Base

class Post(Base):
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author: Mapped['User'] = relationship('User', back_populates='posts')

    media_files = relationship("Media", back_populates="post", cascade="all, delete-orphan")


class Media(Base):
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    post = relationship("Post", back_populates='media_files')
    