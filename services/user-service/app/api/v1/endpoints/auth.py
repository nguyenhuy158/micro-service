from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.config import settings
from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.repositories.user_repository import (
    SqlAlchemyUserRepository,
)
from app.infrastructure.security.jwt_service import JoseJwtService
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.presentation.schemas.user import GoogleLogin, Token, UserCreate, UserResponse
from app.services.google_auth import verify_google_token

router = APIRouter()

_hasher = BcryptPasswordHasher()
_jwt = JoseJwtService()


async def get_user_by_email(db: AsyncSession, email: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    return await repo.get_by_email(email)


async def get_user_by_google_id(db: AsyncSession, google_id: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    return await repo.get_by_google_id(google_id)


async def create_user(db: AsyncSession, user_in: UserCreate) -> Any:
    repo = SqlAlchemyUserRepository(db)
    hashed_password = _hasher.hash(user_in.password)
    return await repo.create(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )


async def create_user_google(
    db: AsyncSession, email: str, google_id: str, full_name: str | None = None
) -> Any:
    repo = SqlAlchemyUserRepository(db)
    return await repo.create(
        email=email,
        google_id=google_id,
        full_name=full_name,
        hashed_password=None,
        role=None,
        is_active=True,
    )


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    user = await repo.get_by_email(email)
    if not user or not user.hashed_password:
        return None
    if not _hasher.verify(password, user.hashed_password):
        return None
    return user


@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = await authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": _jwt.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserResponse)
async def register_new_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = await create_user(db, user_in)
    return user


@router.post("/login/google", response_model=Token)
async def login_google(
    *,
    db: AsyncSession = Depends(get_db),
    google_login: GoogleLogin,
) -> Any:
    google_data = await verify_google_token(google_login.id_token)
    google_id = google_data["sub"]
    email = google_data["email"]
    name = google_data.get("name")

    user = await get_user_by_google_id(db, google_id=google_id)
    if not user:
        user = await get_user_by_email(db, email=email)
        if user:
            user.google_id = google_id
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            user = await create_user_google(
                db, email=email, google_id=google_id, full_name=name
            )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": _jwt.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/google/callback")
async def login_google_callback(
    *,
    db: AsyncSession = Depends(get_db),
    credential: str = Form(...),
) -> Any:
    google_data = await verify_google_token(credential)
    google_id = google_data["sub"]
    email = google_data["email"]
    name = google_data.get("name")

    user = await get_user_by_google_id(db, google_id=google_id)
    if not user:
        user = await get_user_by_email(db, email=email)
        if user:
            user.google_id = google_id
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            user = await create_user_google(
                db, email=email, google_id=google_id, full_name=name
            )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = _jwt.create_access_token(user.email, expires_delta=access_token_expires)

    frontend_url = "http://localhost:3002"
    return RedirectResponse(url=f"{frontend_url}/#token={token}", status_code=303)
