from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from dependencies.dependencies import verify_token
from schemas.follow import FollowCreate, FollowID
from services.follow_service import FollowService

router = APIRouter(
    prefix = "/v1/follows",
    tags = ["follows"],
)

# TODO: Implement OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("", response_model=FollowID)
async def create_follow(
    request_body: FollowCreate,
    current_user = Depends(verify_token),
):
    """
    Creates a follow relationship, with the follower following the followee
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    service = FollowService()
    response = await service.create_follow(request_body)
    if not response:
        raise HTTPException(status_code=400, detail="Follow creation failed")

    return response


@router.delete("/{FollowID}")
async def delete_follow(
    follow_id: int = Path(alias="FollowID"),
    current_user = Depends(verify_token),
):
    """
    Deletes a follow relationship
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    service = FollowService()
    response = await service.delete_follow(follow_id)
    if not response:
        raise HTTPException(status_code=404, detail="Follow not found or deletion failed")
    
    return {"detail": "Follow deleted successfully"}
