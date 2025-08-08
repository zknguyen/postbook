from pydantic import BaseModel, Field


class FollowID(BaseModel):
    follow_id: int = Field(..., alias="FollowID")

class FollowCreate(BaseModel):
    follower_id: int = Field(..., alias="FollowerID")
    followee_id: int = Field(..., alias="FolloweeID")