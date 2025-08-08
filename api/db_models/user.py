from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from db.session import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    firebase_uid = Column(String, unique=True, nullable=False)
    created_at = Column(String, nullable=False)  # Use String for datetime if not using DateTime type
