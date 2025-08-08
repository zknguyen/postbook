from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from schemas.post import Post

class Feed(BaseModel):
    feed_id: int = Field(..., alias="FeedID")
    user_id: int = Field(..., alias="UserID")
    updated_at: datetime = Field(..., alias="UpdatedAt")


class FeedCreate(BaseModel):
    user_id: int = Field(..., alias="UserID")


class FeedID(BaseModel):
    feed_if: int = Field(..., alias="FeedID")


class FeedPost(BaseModel):
    feed_post_id: int = Field(..., alias="FeedPostID")
    feed_id: int = Field(..., alias="FeedID")
    post_id: int = Field(..., alias="PostID")


class FeedPostID(BaseModel):
    feed_post_id: int = Field(..., alias="FeedPostID")


class FeedUpdate(BaseModel):
    post_id: int = Field(..., alias="PostID")
