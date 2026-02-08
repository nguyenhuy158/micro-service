from datetime import timedelta
from typing import Any

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.schemas.user import GoogleLogin, Token, UserCreate, UserResponse
from app.services.google_auth import verify_google_token
from app.services.user_service import (
    authenticate_user,
    create_user,
    create_user_google,
    get_user_by_email,
    get_user_by_google_id,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
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
        "access_token": security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserResponse)
async def register_new_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create new user without the need to be logged in
    """
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
    """
    Login with Google
    """
    google_data = await verify_google_token(google_login.id_token)
    google_id = google_data["sub"]
    email = google_data["email"]
    name = google_data.get("name")

    # Check if user exists by google_id
    user = await get_user_by_google_id(db, google_id=google_id)
    if not user:
        # Check if user exists by email
        user = await get_user_by_email(db, email=email)
        if user:
            # Link google_id to existing user
            user.google_id = google_id
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # Create new user
            user = await create_user_google(
                db, email=email, google_id=google_id, full_name=name
            )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
