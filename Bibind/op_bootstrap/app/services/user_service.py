from app.schemas.user import User, UserCreate


async def list_users() -> list[User]:
    return [User(id=1, email="user@example.com", is_active=True)]


async def create_user(user: UserCreate) -> User:
    return User(id=1, email=user.email, is_active=True)


async def get_user(user_id: int) -> User | None:
    if user_id == 1:
        return User(id=1, email="user@example.com", is_active=True)
    return None


async def update_user(user_id: int, user: UserCreate) -> User | None:
    if user_id == 1:
        return User(id=1, email=user.email, is_active=True)
    return None


async def delete_user(user_id: int) -> bool:
    return user_id == 1
