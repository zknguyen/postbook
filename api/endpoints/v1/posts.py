from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Path, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.post import Post, PostID, PostSearch, PostCreate, PostUpdate
from services.post_service import PostService

router = APIRouter(
    prefix = "/v1/posts",
    tags = ["posts"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{PostID}", response_model=Post)
async def get_post(post_id: int = Path(alias="PostID")):
    """
    Get a post by its ID.
    """
    service = PostService()
    response = await service.get_post(post_id)
    if not response:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return response


@router.get("", response_model=list[Post])
async def search_posts(
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    user_id: int | None = Query(None, alias="UserID"),
):
    """
    Search for posts based on the query parameters.
    """
    service = PostService()
    response = await service.search_posts(limit, offset, user_id)
    if not response:
        raise HTTPException(status_code=404, detail="No posts found")
    
    return response


@router.post("", response_model=PostID)
async def create_post(request_body: PostCreate):
    """
    Create a new post.
    """
    service = PostService()
    response = await service.create_post(request_body)
    if not response:
        raise HTTPException(status_code=400, detail="Failed to create post")

    return response


@router.put("/{PostID}", response_model=PostID)
async def update_post(request_body: PostUpdate, post_id: int = Path(alias="PostID")):
    """
    Update an existing post.
    """
    service = PostService()
    response = await service.update_post(post_id, request_body)
    if not response:
        raise HTTPException(status_code=404, detail="Post not found or update failed")
    
    return response


@router.delete("/{PostID}")
async def delete_post(post_id: int = Path(alias="PostID")):
    """
    Delete a post by its ID.
    """
    service = PostService()
    response = await service.delete_post(post_id)
    if not response:
        raise HTTPException(status_code=404, detail="Post not found or deletion failed")
    
    return {"detail": "Post deleted successfully"}