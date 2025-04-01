from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    creator_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_private = Column(Boolean, default=False)
    tags = Column(ARRAY(String), default=[])
