from typing import Optional

import sqlalchemy as sa
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from firebase_admin.auth import verify_id_token
from sqlalchemy.exc import DataError
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_engine
from db_models.user import User
from schemas.user import UserCreate


class UserService:
    def __init__(self):
        self.bearer_scheme = HTTPBearer(auto_error=False)

    async def get_user(self, user_id: int):
        statement = sa.select(User).where(User.user_id == user_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            user = response.scalar_one_or_none()
        if not user:
            return None
        return {
            "UserID": user.user_id,
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "Username": user.username,
            "Email": user.email,
            "FirebaseUID": user.firebase_uid,
        }

    async def get_user_by_firebase_id(self, firebase_id: str):
        statement = sa.select(User).where(User.firebase_uid == firebase_id)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            user = response.scalar_one_or_none()

        if not user:
            return None
        return {
            "UserID": user.user_id,
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "Username": user.username,
            "Email": user.email,
            "FirebaseUID": user.firebase_uid,
        }

    async def create_user(self, body: UserCreate):
        statement = (
            sa.insert(User)
            .values(
                username=body.username,
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
                firebase_uid=body.firebase_uid,
            )
            .returning(User.user_id)
        )

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            user_id = response.scalar_one()
            await session.commit()
        if not user_id:
            raise DataError("Failed to create user.")

        return {"UserID": user_id}