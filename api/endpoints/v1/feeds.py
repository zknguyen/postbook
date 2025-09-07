from typing import List
from typing import Union
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from dependencies.dependencies import verify_token
from schemas.feed import FeedID, FeedUpdate
from schemas.post import Post
from services.feed_service import FeedService


router = APIRouter(
    prefix = "/v1/feeds",
    tags = ["feeds"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{UserID}", response_model=Dict[str, Union[int, List[Post]]])
async def get_feed(
    user_id: int = Path(alias="UserID"),
    current_user = Depends(verify_token),
):
    """
    Gets all FeedPosts for a given user's feed.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = FeedService()
        response = await service.get_feed(user_id)
        if not response:
            raise HTTPException(status_code=404, detail="Feed not found")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{UserID}", response_model = FeedID)
async def create_feed(
    user_id: int = Path(alias="UserID"),
    current_user = Depends(verify_token),
):
    """
    Gets all FeedPosts for a given user's feed.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = FeedService()
        response = await service.create_feed(user_id)
        if not response:
            raise HTTPException(status_code=400, detail="Failed to create feed")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/posts/{UserID}")
async def update_feeds(
    request_body: FeedUpdate,
    user_id: int = Path(alias="UserID"),
    current_user = Depends(verify_token),
):
    """
    Pushes a post to feeds of all followers of a given user.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = FeedService()
        response = await service.update_feeds(user_id, request_body)
        if not response:
            raise HTTPException(status_code=400, detail="Failed to create feed post")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
