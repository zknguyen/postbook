from typing import Union

from fastapi import APIRouter, HTTPException, Header, Path, Query
from fastapi.security import OAuth2PasswordBearer

from schemas.user import User, UserID, UserCreate
from services.feed_service import FeedService
from services.user_service import UserService

router = APIRouter(
    prefix = "/v1/users",
    tags = ["users"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=Union[User, None])
async def get_current_user(authorization: str = Header(...)):
    service = UserService()
    response = await service.verify_current_user(authorization.split(" ")[1])

    if not response:
        return 

    return response


@router.get("/{UserID}", response_model=User)
async def get_user(
    user_id: int = Path(alias="UserID")
):
    """
    Get a user by their ID.
    """
    service = UserService()
    response = await service.get_user(user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")

    return response


@router.get("", response_model=list[User])
async def get_users_by_field(
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    username: str | None = Query(None, alias="Username"),
    first_name: str | None = Query(None, alias="FirstName"),
    last_name: str | None = Query(None, alias="LastName"),
    firebase_uid: str | None = Query(None, alias="FirebaseUID"),
    email: str | None = Query(None, alias="Email"),
):
    """
    Search for users based on the request body.
    """
    service = UserService()
    response = await service.get_users_by_field(limit, offset, username, first_name, last_name, firebase_uid, email)
    if not response:
        raise HTTPException(status_code=404, detail="No users found")

    return response


@router.post("", response_model=UserID)
async def create_user(
    request_body: UserCreate
):
    """
    Create a new user and corresponding feed.
    """
    user_service = UserService()
    user_response = await user_service.create_user(request_body)
    if not user_response:
        raise HTTPException(status_code=400, detail="User creation failed")
    
    feed_service = FeedService()
    feed_response = await feed_service.create_feed(user_response["UserID"])
    if not feed_response:
        raise HTTPException(status_code=400, detail="Feed creation failed")

    return user_response
    