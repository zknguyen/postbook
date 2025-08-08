from typing import List
from typing import Union
from typing import Dict

from fastapi import APIRouter, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from schemas.feed import FeedID, FeedUpdate
from schemas.post import Post
from services.feed_service import FeedService


router = APIRouter(
    prefix = "/v1/feeds",
    tags = ["feeds"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{UserID}", response_model=Dict[str, Union[int, List[Post]]])
async def get_feed(user_id: int = Path(alias="UserID")):
    """
    Gets all FeedPosts for a given user's feed.
    """
    service = FeedService()
    response = await service.get_feed(user_id)
    if not response:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    return response


@router.post("/{UserID}", response_model = FeedID)
async def create_feed(user_id: int = Path(alias="UserID")):
    """
    Gets all FeedPosts for a given user's feed.
    """
    service = FeedService()
    response = await service.create_feed(user_id)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create feed")
    
    return response


@router.post("/posts/{UserID}")
async def update_feeds(
    request_body: FeedUpdate,
    user_id: int = Path(alias="UserID"),
):
    """
    Pushes a post to feeds of all followers of a given user.
    """
    service = FeedService()
    response = await service.update_feeds(user_id, request_body)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create feed post")
    
    return response
