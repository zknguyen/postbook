from fastapi import APIRouter, HTTPException, Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer

from dependencies.dependencies import verify_token
from schemas.post import Post, PostID, PostCreate, PostUpdate
from services.post_service import PostService

router = APIRouter(
    prefix = "/v1/posts",
    tags = ["posts"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{PostID}", response_model=Post)
async def get_post(
    post_id: int = Path(alias="PostID"),
    current_user = Depends(verify_token),
):
    """
    Get a post by its ID.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = PostService()
        response = await service.get_post(post_id)
        if not response:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[Post])
async def search_posts(
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    user_id: int | None = Query(None, alias="UserID"),
):
    """
    Search for posts based on the query parameters.
    """
    try:
        service = PostService()
        response = await service.search_posts(limit, offset, user_id)
        if not response:
            raise HTTPException(status_code=404, detail="No posts found")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=PostID)
async def create_post(
    request_body: PostCreate,
    current_user = Depends(verify_token),
):
    """
    Create a new post.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    service = PostService()
    response = await service.create_post(request_body)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create post")

    return response


@router.put("/{PostID}", response_model=PostID)
async def update_post(
    request_body: PostUpdate,
    post_id: int = Path(alias="PostID"),
    current_user = Depends(verify_token),
):
    """
    Update an existing post.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = PostService()
        response = await service.update_post(post_id, request_body)
        if not response:
            raise HTTPException(status_code=404, detail="Post not found or update failed")
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{PostID}")
async def delete_post(
    post_id: int = Path(alias="PostID"),
    current_user = Depends(verify_token),
):
    """
    Delete a post by its ID.
    """
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        service = PostService()
        response = await service.delete_post(post_id)
        if not response:
            raise HTTPException(status_code=404, detail="Post not found or deletion failed")
        
        return {"detail": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))