"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.auth import LoginRequest, Token, RefreshToken, Permissions
from app.schemas.user import User
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest) -> JSONResponse:
    token = await auth_service.login(credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=token.dict())


@router.get("/me", response_model=User)
async def me(user: User = Depends(auth_service.get_current_user)) -> User:
    return user


@router.post("/refresh", response_model=Token)
async def refresh(token: RefreshToken) -> JSONResponse:
    new_token = await auth_service.refresh_token(token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=new_token.dict())


@router.post("/logout")
async def logout() -> JSONResponse:
    await auth_service.logout()
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"detail": "logged out"}
    )


@router.get("/permissions", response_model=Permissions)
async def permissions() -> Permissions:
    return await auth_service.get_permissions()
