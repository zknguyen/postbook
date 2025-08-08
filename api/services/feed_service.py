from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.exc import DataError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_engine
from db_models.feed import Feed # TODO: Fix this and the Feed schema names
from db_models.feed_post import FeedPost
from db_models.follow import Follow
from db_models.post import Post
from schemas.feed import FeedUpdate

class FeedService:
    def __init__(self):
        pass

    async def get_feed(self, user_id: int):
        statement = (
            sa.select(Feed.feed_id)
            .where(Feed.user_id == user_id)
        )
        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            feed_id = response.scalar_one_or_none()
        if not feed_id:
            raise NoResultFound("Feed not found for provided UserID")
        
        statement = (
            sa.select(Post)
            .where(
                Post.post_id.in_(
                    sa.select(FeedPost.post_id)
                    .where(FeedPost.feed_id == feed_id)
                )
            )
        )
        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            feed_posts = response.scalars()
        if not feed_posts:
            return None

        return {
            "FeedID": feed_id,
            "FeedPosts": [
                {
                    "PostID": feed_post.post_id,
                    "UserID": feed_post.user_id,
                    "TextContent": feed_post.text_content,
                } for feed_post in feed_posts
            ]
        }

    async def create_feed(self, user_id: int):
        current_datetime = datetime.now()
        statement = (
            sa.insert(Feed)
            .values(
                user_id=user_id,
                updated_at=current_datetime,
            )
            .returning(Feed.feed_id)
        )
        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            feed_id = response.scalar_one()
            await session.commit()
        if not feed_id:
            raise IntegrityError("Failed to create feed")
        
        return {"FeedID": feed_id}
    
    async def update_feeds(self, user_id: int, body: FeedUpdate):
        # Get list of follower_ids
        statement = (
            sa.select(Feed.feed_id)
            .where(
                sa.or_(
                    Feed.user_id == user_id,
                    Feed.user_id.in_(
                        sa.select(Follow.follower_id)
                        .where(Follow.followee_id == user_id)
                    ),
                )
            )
        )
        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            feed_ids = response.scalars().all()
        # TODO: Handle bad response

        # Push post to all followers' feeds
        if feed_ids:
            async with AsyncSession(async_engine) as session:
                await session.execute(
                    sa.insert(FeedPost).returning(FeedPost.feed_post_id),
                    [
                        {"feed_id": feed_id, "post_id": body.post_id} for feed_id in feed_ids
                    ],
                )
                await session.commit()
        
        # TODO: handle this return
        return {"UserID": user_id}
