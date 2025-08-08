from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(..., alias="UserID")
    username: str = Field(..., alias="Username")
    first_name: str = Field(..., alias="FirstName")
    last_name: str = Field(..., alias="LastName")
    email: str = Field(..., alias="Email")
    firebase_uid: str = Field(..., alias="FirebaseUID")


class UserID(BaseModel):
    user_id: int = Field(..., alias="UserID")


class UserCreate(BaseModel):
    username: str = Field(..., alias="Username")
    first_name: str = Field(..., alias="FirstName")
    last_name: str = Field(..., alias="LastName")
    email: str = Field(..., alias="Email")
    firebase_uid: str = Field(..., alias="FirebaseUID")