from typing import Union

from fastapi import APIRouter, HTTPException, Depends, Header, Path, Query

from dependencies.dependencies import verify_token
from schemas.user import User, UserID, UserCreate
from services.feed_service import FeedService
from services.user_service import UserService

router = APIRouter(
    prefix = "/v1/users",
    tags = ["users"],
)


@router.get("/{UserID}", response_model=User)
async def get_user(
    current_user = Depends(verify_token),
    user_id: int = Path(alias="UserID"),
):
    """
    Get a user by their ID or Firebase UID.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    service = UserService()
    response = await service.get_user(user_id)

    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@router.get("/by-firebase-id/{FirebaseUID}")
async def get_user_by_firebase_id(firebase_id: str = Path(alias="FirebaseUID")):
    """
    Get a user by their Firebase UID.
    """
    service = UserService()
    response = await service.get_user_by_firebase_id(firebase_id)

    # TODO: implement some sort of error handling
    # if not response:
    #     raise HTTPException(status_code=404, detail="User not found")
    return response


@router.post("", response_model=UserID)
async def create_user(
    request_body: UserCreate,
    current_user = Depends(verify_token),
):
    """
    Create a new user and corresponding feed.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_service = UserService()
    user_response = await user_service.create_user(request_body)
    if not user_response:
        raise HTTPException(status_code=400, detail="User creation failed")
    
    feed_service = FeedService()
    feed_response = await feed_service.create_feed(user_response["UserID"])
    if not feed_response:
        raise HTTPException(status_code=400, detail="Feed creation failed")

    return user_response
    