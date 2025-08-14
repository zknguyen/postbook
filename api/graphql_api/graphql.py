import strawberry
from typing import List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from db_models.comment import Comment as CommentModel
from db_models.feed import Feed as FeedModel
from db_models.feed_post import FeedPost as FeedPostModel
from db_models.like import Like as LikeModel
from db_models.post import Post as PostModel
from db_models.user import User as UserModel
from db.session import async_engine


@strawberry.type
class User:
    user_id: strawberry.ID
    username: str
    first_name: str
    last_name: str
    email: str
    firebase_uid: str
    created_at: str  # Use String for datetime if not using DateTime type


@strawberry.type
class Like:
    like_id: int
    post_id: int
    user_id: int


@strawberry.type
class Comment:
    comment_id: int
    post_id: int
    user_id: int
    text_content: str
    created_at: str  # Use String for datetime if not using DateTime type


# TODO: Find a way to move likes to here and then have feedpost reference it
@strawberry.type
class Post:
    post_id: strawberry.ID
    user_id: strawberry.ID
    text_content: str
    num_likes: int
    media_url: str
    created_at: str  # Use String for datetime if not using DateTime type

    @strawberry.field
    async def likes(self) -> List[Like]:
        async with AsyncSession(async_engine) as session:
            statement = sa.select(LikeModel).where(LikeModel.post_id == int(self.post_id), LikeModel.active)
            response = await session.execute(statement)
            likes = response.scalars()

            return [
                Like(
                    like_id=like.like_id,
                    post_id=like.post_id,
                    user_id=like.user_id,
                ) for like in likes
            ]

    @strawberry.field
    async def comments(self) -> List[Comment]:
        async with AsyncSession(async_engine) as session:
            statement = sa.select(CommentModel).where(CommentModel.post_id == int(self.post_id))
            response = await session.execute(statement)
            comments = response.scalars()

            return [
                Comment(
                    comment_id=comment.comment_id,
                    post_id=comment.post_id,
                    user_id=comment.user_id,
                    text_content=comment.text_content,
                    created_at=comment.created_at,
                ) for comment in comments
            ]


@strawberry.type
class FeedPost:
    feed_post_id: strawberry.ID
    feed_id: strawberry.ID
    post_id: strawberry.ID
    
    @strawberry.field
    async def user(self) -> User:
        # TODO: Handle errors
        async with AsyncSession(async_engine) as session:
            statement = (
                sa.select(UserModel)
                .where(UserModel.user_id == (
                    sa.select(PostModel.user_id)
                    .where(PostModel.post_id == int(self.post_id))
                ))
            )
            response = await session.execute(statement)
            user = response.scalar_one_or_none()

            return User(
                user_id=user.user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                firebase_uid=user.firebase_uid,
                created_at=user.created_at
            ) if user else None
        
    @strawberry.field
    async def post(self) -> Post:
        # TODO: Handle errors
        async with AsyncSession(async_engine) as session:
            statement = sa.select(PostModel).where(PostModel.post_id == int(self.post_id))
            response = await session.execute(statement)
            post = response.scalar_one_or_none()

            return Post(
                post_id=post.post_id,
                text_content=post.text_content,
                user_id=post.user_id,
                num_likes=post.num_likes,
                media_url=post.media_url,
                created_at=post.created_at,
            ) if post else None


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, user_id: strawberry.ID) -> User:
        # TODO: Handle errors
        async with AsyncSession(async_engine) as session:
            statement = sa.select(UserModel).where(UserModel.user_id == int(user_id))
            response = await session.execute(statement)
            user = response.scalar_one_or_none()

            return User(username=user.username) if user else None

    @strawberry.field
    async def post(self, post_id: strawberry.ID) -> Post:
        async with AsyncSession(async_engine) as session:
            statement = sa.select(PostModel).where(PostModel.post_id == int(post_id))
            response = await session.execute(statement)
            post = response.scalar_one_or_none()

            return Post(
                post_id=post.post_id,
                text_content=post.text_content,
                user_id=post.user_id,
                num_likes=post.num_likes,
                media_url=post.media_url,
                created_at=post.created_at,
            ) if post else None
        
    @strawberry.field
    async def posts(self, user_id: strawberry.ID) -> List[Post]:
        async with AsyncSession(async_engine) as session:
            statement = sa.select(PostModel).where(PostModel.user_id == int(user_id))
            response = await session.execute(statement)
            posts = response.scalars().all()

            return [
                Post(
                    post_id=post.post_id,
                    text_content=post.text_content,
                    user_id=post.user_id,
                    num_likes=post.num_likes,
                    media_url=post.media_url,
                    created_at=post.created_at,
                ) for post in posts
            ]

    @strawberry.field
    async def feed_posts(self, user_id: strawberry.ID) -> List[FeedPost]:
        # TODO: Handle errors
        async with AsyncSession(async_engine) as session:
            statement = sa.select(FeedPostModel).where(
                FeedPostModel.feed_id == (
                    sa.select(FeedModel.feed_id)
                    .where(FeedModel.user_id == int(user_id))
                )
            )
            response = await session.execute(statement)
            feed_posts = response.scalars().all()

            return [
                FeedPost(
                    feed_post_id=feed_post.feed_post_id,
                    feed_id=feed_post.feed_id,
                    post_id=feed_post.post_id
                ) for feed_post in feed_posts
            ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    # TODO: Can we find a way to simplify this?
    async def like_post(self, post_id: strawberry.ID, user_id: strawberry.ID) -> FeedPost:
        async with AsyncSession(async_engine) as session:
            statement = (
                sa.insert(LikeModel)
                .values(post_id=int(post_id), user_id=int(user_id))
                .returning(LikeModel.like_id)
            )
            response = await session.execute(statement)
            like_id = response.scalar_one_or_none()

            if like_id is None:
                raise Exception("Failed to create like")
            
            statement = (
                sa.update(PostModel)
                .where(PostModel.post_id == int(post_id))
                .values(num_likes=PostModel.num_likes + 1)
            )
            await session.execute(statement)
            await session.commit()

            statement = (
                sa.select(FeedPostModel)
                .where(
                    FeedPostModel.post_id == int(post_id),
                    FeedPostModel.feed_id == (
                        sa.select(FeedModel.feed_id)
                        .where(FeedModel.user_id == int(user_id))
                    )
                )
            )
            response = await session.execute(statement)
            feed_post = response.scalar_one()

            if feed_post is None:
                raise Exception("Failed fetch feed post")

            return feed_post
        
    @strawberry.mutation
    async def unlike_post(self, post_id: strawberry.ID, user_id: strawberry.ID) -> FeedPost:
        async with AsyncSession(async_engine) as session:
            statement = (
                sa.update(LikeModel)
                .where(LikeModel.post_id == int(post_id), LikeModel.user_id == int(user_id))
                .values(active=False)
            )
            await session.execute(statement)
            
            statement = (
                sa.update(PostModel)
                .where(PostModel.post_id == int(post_id))
                .values(num_likes=PostModel.num_likes - 1)
            )
            await session.execute(statement)
            await session.commit()

            statement = (
                sa.select(FeedPostModel)
                .where(
                    FeedPostModel.post_id == int(post_id),
                    FeedPostModel.feed_id == (
                        sa.select(FeedModel.feed_id)
                        .where(FeedModel.user_id == int(user_id))
                    )
                )
            )
            response = await session.execute(statement)
            feed_post = response.scalar_one()

            if feed_post is None:
                raise Exception("Failed fetch feed post")

            return feed_post
        
    @strawberry.mutation
    async def add_comment(self, post_id: strawberry.ID, user_id: strawberry.ID, text_content: str) -> Comment:
        async with AsyncSession(async_engine) as session:
            statement = (
                sa.insert(CommentModel)
                .values(post_id=int(post_id), user_id=int(user_id), text_content=text_content)
                .returning(CommentModel.comment_id)
            )
            response = await session.execute(statement)
            comment_id = response.scalar_one()

            await session.commit()

            if comment_id is None:
                raise Exception("Failed to create comment")

            statement = (
                sa.select(CommentModel)
                .where(CommentModel.comment_id == comment_id)
            )
            response = await session.execute(statement)
            comment = response.scalar_one()
            
            
            return Comment(
                comment_id=comment.comment_id,
                post_id=comment.post_id,
                user_id=comment.user_id,
                text_content=comment.text_content,
                created_at=comment.created_at
            )
        

schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_router = GraphQLRouter(schema)
