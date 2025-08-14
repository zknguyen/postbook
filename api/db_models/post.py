from sqlalchemy import Column, Integer, String

from db.session import Base


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    text_content = Column(String, nullable=False)
    num_likes = Column(Integer, nullable=False, default=0)
    media_url = Column(String, nullable=True)
    created_at = Column(String, nullable=False)  # Use String for datetime if not using DateTime type
