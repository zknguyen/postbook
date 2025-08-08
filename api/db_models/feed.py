from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from db.session import Base


class Feed(Base):
    __tablename__ = "feeds"
    feed_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)  # Use String for datetime if not using DateTime type
    updated_at = Column(DateTime, nullable=False)
