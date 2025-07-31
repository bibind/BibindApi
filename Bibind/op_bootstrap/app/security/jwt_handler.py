"""Utility functions to generate and decode JWT tokens."""

from datetime import datetime, timedelta
from typing import Any, Dict

import jwt

from app.settings import settings


ALGORITHM = "HS256"


def create_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """Return a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> Dict[str, Any] | None:
    """Decode a JWT token and return the payload."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
