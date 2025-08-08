from sqlalchemy import Column, Integer

from db.session import Base


class FeedPost(Base):
    __tablename__ = "feed_posts"
    feed_post_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    feed_id = Column(Integer, nullable=False)
    post_id = Column(Integer, nullable=False)
