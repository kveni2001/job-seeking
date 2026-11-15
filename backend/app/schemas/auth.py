from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user fields shared across requests and responses."""
    email: EmailStr = Field(..., description="User's unique email address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="User's full name")
    is_active: bool = Field(default=True, description="Whether the user account is active")


class UserCreate(BaseModel):
    """Payload for user registration / creation."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="Plaintext password (min 8 chars)")
    full_name: Optional[str] = Field(default=None, max_length=255, description="User's full name")


class UserRegister(UserCreate):
    """Alias for user sign up."""
    pass


class UserLogin(BaseModel):
    """Payload for user login authentication."""
    email: EmailStr = Field(..., description="Registered email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """Payload for updating user profile."""
    email: Optional[EmailStr] = Field(default=None, description="New email address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="Updated full name")
    password: Optional[str] = Field(default=None, min_length=8, max_length=128, description="New password")
    is_active: Optional[bool] = Field(default=None, description="Account active status")


class UserPasswordChange(BaseModel):
    """Payload for changing current password."""
    current_password: str = Field(..., description="Existing plaintext password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New plaintext password (min 8 chars)")


class UserResponse(UserBase):
    """Public user response schema."""
    id: UUID = Field(..., description="User's unique UUID")
    is_superuser: bool = Field(default=False, description="Superuser privilege flag")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Account last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """OAuth2 / JWT access token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    refresh_token: Optional[str] = Field(default=None, description="JWT refresh token")
    expires_in: Optional[int] = Field(default=None, description="Token lifetime in seconds")


class TokenPayload(BaseModel):
    """Parsed JWT payload structure."""
    sub: Optional[str] = Field(default=None, description="Subject (User UUID string)")
    exp: Optional[int] = Field(default=None, description="Expiration UNIX timestamp")


class RefreshTokenRequest(BaseModel):
    """Request payload to exchange a refresh token for a new access token."""
    refresh_token: str = Field(..., description="Valid refresh token")
