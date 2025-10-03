"""
Pydantic Schemas

Request and response models for API validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# User Schemas

class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$",
        description="Username (alphanumeric, hyphens, underscores only)",
    )


class UserCreate(UserBase):
    """Schema for user creation request."""

    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
    )


class UserUpdate(BaseModel):
    """Schema for user update request."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$",
    )
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


class UserList(BaseModel):
    """Schema for paginated user list response."""

    items: list[UserResponse]
    total: int
    skip: int
    limit: int


# Authentication Schemas

class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Schema for decoded token data."""

    username: Optional[str] = None
    user_id: Optional[UUID] = None
