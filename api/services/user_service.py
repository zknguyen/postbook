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

    async def verify_current_user(self, token: str):
        try:
            # Verify JWT with Firebase SDK
            if not token:
                raise ValueError("Token not provided")
            firebase_user = verify_id_token(token)

            users = await self.get_users_by_field(limit=1, offset=0, firebase_uid=firebase_user.get("uid"))
        
            return users[0] if users else None

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not logged in or Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

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

    async def get_users_by_field(
        self,
        limit: int,
        offset: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        firebase_uid: Optional[str] = None,
        email: Optional[str] = None,
    ):
        statement = (
            sa.select(User)
            .limit(limit)
            .offset(offset)
            .order_by(User.user_id)
        )

        if username:
            statement = statement.where(User.username.ilike(f"%{username}%"))
        if first_name:
            statement = statement.where(User.first_name.ilike(f"%{first_name}%"))
        if last_name:
            statement = statement.where(User.last_name.ilike(f"%{last_name}%"))
        if email:
            statement = statement.where(User.email.ilike(f"%{email}%"))
        if firebase_uid:
            statement = statement.where(User.firebase_uid == firebase_uid)

        async with AsyncSession(async_engine) as session:
            response = await session.execute(statement)
            users = response.scalars()

        return [
            {
                "UserID": user.user_id,
                "FirstName": user.first_name,
                "LastName": user.last_name,
                "Username": user.username,
                "Email": user.email,
                "FirebaseUID": user.firebase_uid,

            } for user in users
        ]

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