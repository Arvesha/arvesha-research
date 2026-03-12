from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token


async def register_user(request: RegisterRequest, db: AsyncSession) -> User:
    repo = UserRepository(db)
    if await repo.get_by_username(request.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    if await repo.get_by_email(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        username=request.username,
        email=request.email,
        hashed_password=get_password_hash(request.password),
    )
    return await repo.create(user)


async def login_user(request: LoginRequest, db: AsyncSession) -> TokenResponse:
    repo = UserRepository(db)
    user = await repo.get_by_username(request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)
