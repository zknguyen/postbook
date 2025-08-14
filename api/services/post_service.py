from typing import Optional

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_engine
from db_models.post import Post
from schemas.post import PostCreate, PostID, PostUpdate


class PostService:
    def __init__(self):
        pass

    async def get_post(self, post_id: int):
        statement = sa.select(Post.post_id, Post.user_id, Post.text_content).where(Post.post_id == post_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            post = response.fetchone()
        if post is None:
            raise NoResultFound(f"Post with ID {post_id} not found.")

        return {
            "PostID": post.post_id,
            "UserID": post.user_id,
            "TextContent": post.text_content,
            "NumLikes": post.num_likes,
            "MediaURL": post.media_url,
        }

    async def search_posts(self, limit: int, offset: int, user_id: Optional[int] = None):
        statement = (
            sa.select(Post.post_id, Post.user_id, Post.text_content)
            .limit(limit)
            .offset(offset)
        )

        if user_id:
            statement = statement.where(Post.user_id == user_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            posts = response.fetchall()
        if not posts:
            raise NoResultFound("No posts found matching the search criteria.")

        return [
            {
                "PostID": post.post_id,
                "UserID": post.user_id,
                "TextContent": post.text_content,
                "NumLikes": post.num_likes,
                "MediaURL": post.media_url,
            } for post in posts
        ]

    async def create_post(self, request_body: PostCreate):
        statement = (
            sa.insert(Post)
            .values(
                user_id=request_body.user_id,
                text_content=request_body.text_content,
                media_url=request_body.media_url,
            )
            .returning(Post.post_id)
        )

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            post_id = response.scalar_one_or_none()
            await session.commit()
        if not post_id:
            raise IntegrityError("Failed to create post.")

        return {"PostID": post_id}

    async def update_post(self, post_id: int, request_body: PostUpdate):
        statement = (
            sa.update(Post)
            .where(Post.post_id == post_id)
            .values(
                text_content=request_body.text_content,
            )
            .returning(Post.post_id)
        )

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            updated_post_id = response.scalar_one_or_none()
            await session.commit()
        if not updated_post_id:
            raise IntegrityError(f"Post with ID {post_id} not found or update failed.")

        return {"PostID": updated_post_id}

    async def delete_post(self, post_id: int):
        statement = sa.delete(Post).where(Post.post_id == post_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            await session.commit()
        if response.rowcount == 0:
            raise NoResultFound(f"Post with ID {post_id} not found.")
        
        return {"PostID": post_id}