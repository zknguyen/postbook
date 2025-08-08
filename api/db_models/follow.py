from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

from db.session import Base


class Follow(Base):
    __tablename__ = "follows"
    follow_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    follower_id = Column(Integer, nullable=False)
    followee_id = Column(Integer, nullable=False)
