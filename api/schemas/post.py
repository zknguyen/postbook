from typing import Optional

from pydantic import BaseModel, Field


class Post(BaseModel):
    post_id: int = Field(..., alias="PostID")
    user_id: int = Field(..., alias="UserID")
    text_content: str = Field(..., alias="TextContent")
    num_likes: int = Field(..., alias="NumLikes")


class PostID(BaseModel):
    post_id: int = Field(..., alias="PostID")


class PostSearch(BaseModel):
    username: Optional[str] = Field(default=None, alias="Username")


class PostCreate(BaseModel):
    user_id: int = Field(..., alias="UserID")
    text_content: str = Field(..., alias="TextContent")

class PostUpdate(BaseModel):
    text_content: Optional[str] = Field(default=None, alias="TextContent")
