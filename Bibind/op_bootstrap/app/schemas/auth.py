"""Pydantic models for authentication."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    refresh_token: str


class Permissions(BaseModel):
    permissions: list[str]
