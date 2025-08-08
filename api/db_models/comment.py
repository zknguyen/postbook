from sqlalchemy import Column, Integer, String

from db.session import Base


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    text_content = Column(String, nullable=False)
    created_at = Column(String, nullable=False)  # Use String for datetime if not using DateTime type
