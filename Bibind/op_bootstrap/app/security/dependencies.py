"""FastAPI dependencies for authentication and authorization."""

from fastapi import Depends, HTTPException, status

from app.schemas.user import User
from app.security.jwt_handler import decode_token
from app.security.oauth2_scheme import oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Return the current user extracted from the JWT token."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return User(
        id=payload.get("sub"),
        email=payload.get("email"),
        is_active=True,
        role=payload.get("role"),
    )


def role_required(required_role: str):
    """Dependency factory verifying the role of the current user."""

    async def _checker(token: str = Depends(oauth2_scheme)) -> User:
        payload = decode_token(token)
        if not payload or payload.get("role") != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return User(
            id=payload.get("sub"),
            email=payload.get("email"),
            is_active=True,
            role=payload.get("role"),
        )

    return _checker
