"""Business logic for authentication."""

from datetime import timedelta
from typing import Optional

from app.clients.keycloak_client import KeycloakClient
from app.schemas.auth import LoginRequest, Token, RefreshToken, Permissions
from app.schemas.user import User
from app.security.jwt_handler import create_token, decode_token
from app.security.role_permissions import ROLE_PERMISSIONS
from app.settings import settings

# In-memory user store used for examples and tests
_FAKE_USERS = {
    "user@example.com": {"id": 1, "password": "password", "role": "user"},
    "admin@example.com": {"id": 2, "password": "admin", "role": "admin"},
}

_keycloak_client: Optional[KeycloakClient] = None


def _get_keycloak() -> KeycloakClient:
    global _keycloak_client
    if _keycloak_client is None:
        _keycloak_client = KeycloakClient()
    return _keycloak_client


async def login(credentials: LoginRequest) -> Optional[Token]:
    """Authenticate a user locally or via Keycloak."""
    user = _FAKE_USERS.get(credentials.email)
    if user and credentials.password == user["password"]:
        claims = {
            "sub": user["id"],
            "email": credentials.email,
            "role": user["role"],
        }
        access = create_token(
            claims, timedelta(minutes=settings.access_token_expire_minutes)
        )
        refresh = create_token(
            claims, timedelta(minutes=settings.refresh_token_expire_minutes)
        )
        return Token(access_token=access, refresh_token=refresh)

    # fallback to Keycloak
    try:
        kc = _get_keycloak()
        token = kc.login(credentials.email, credentials.password)
        return Token(
            access_token=token["access_token"],
            refresh_token=token.get("refresh_token"),
        )
    except Exception:
        return None


async def refresh_token(payload: RefreshToken) -> Token:
    """Refresh an access token using the refresh token."""
    data = decode_token(payload.refresh_token)
    if not data:
        # try keycloak refresh
        try:
            kc = _get_keycloak()
            token = kc.refresh(payload.refresh_token)
            return Token(
                access_token=token["access_token"],
                refresh_token=token.get("refresh_token"),
            )
        except Exception as exc:  # pragma: no cover - fallback path
            raise ValueError("Invalid refresh token") from exc

    access = create_token(
        {k: data[k] for k in ["sub", "role", "email"]},
        timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=access, refresh_token=payload.refresh_token)


async def logout() -> bool:
    """Logout placeholder."""
    return True


async def get_current_user(token: str) -> User:
    data = decode_token(token)
    if not data:
        raise ValueError("Invalid token")
    return User(
        id=data.get("sub"),
        email=data.get("email"),
        is_active=True,
        role=data.get("role"),
    )


async def get_permissions(role: str) -> Permissions:
    perms = ROLE_PERMISSIONS.get(role, [])
    return Permissions(permissions=perms)
