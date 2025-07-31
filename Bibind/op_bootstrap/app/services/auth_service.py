from app.schemas.auth import LoginRequest, Token, RefreshToken, Permissions
from app.schemas.user import User


async def login(credentials: LoginRequest) -> Token:
    """Return a fake JWT token."""
    return Token(access_token="fake-token", token_type="bearer")


async def get_current_user() -> User:
    """Return a mock current user."""
    return User(id=1, email="user@example.com", is_active=True)


async def refresh_token(_: RefreshToken) -> Token:
    """Return a refreshed token."""
    return Token(access_token="refreshed-token", token_type="bearer")


async def logout() -> bool:
    """Mock logout action."""
    return True


async def get_permissions() -> Permissions:
    """Return mock permissions."""
    return Permissions(permissions=["read", "write"])
