from sqlalchemy import Column, Integer, Boolean

from db.session import Base


# TODO: Add createdAt here and all other models
class Like(Base):
    __tablename__ = "likes"
    like_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
