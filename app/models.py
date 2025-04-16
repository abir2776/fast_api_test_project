from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    url = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)
