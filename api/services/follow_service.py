from typing import Optional

import sqlalchemy as sa
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from firebase_admin.auth import verify_id_token
from sqlalchemy.exc import NoResultFound, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_engine
from db_models.follow import Follow
from schemas.follow import FollowCreate


class FollowService:
    def __init__(self):
        pass

    async def create_follow(self, body: FollowCreate):
        statement = (
            sa.insert(Follow)
            .values(
                follower_id=body.follower_id,
                followee_id=body.followee_id,
            )
            .returning(Follow.follow_id)
        )
        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            follow_id = response.scalar_one()
            await session.commit()
        if not follow_id:
            raise DataError("Failed to create follow relationship.")

        return {"FollowID": follow_id}

    async def delete_follow(self, follow_id: int):
        statement = sa.delete(Follow).where(Follow.follow_id == follow_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            await session.commit()
        if response.rowcount == 0:
            raise NoResultFound(f"Follow with ID {follow_id} not found.")
        
        return {"FollowID": follow_id}