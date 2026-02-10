import os
import shutil
import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.models.user import User
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.presentation.deps import get_current_active_user
from app.presentation.schemas.user import (
    PasswordChange,
    TOTPSetup,
    TOTPVerify,
    UserResponse,
    UserUpdate,
)
from app.services import user_service
from app.services.user_service import verify_totp_code

router = APIRouter()

_hasher = BcryptPasswordHasher()


@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if user_in.email and user_in.email != current_user.email:
        existing = await user_service.get_user_by_email(db, email=user_in.email)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )
    user = await user_service.update_user(db, db_user=current_user, user_in=user_in)
    return user


@router.post("/me/password", response_model=UserResponse)
async def change_password_me(
    *,
    db: AsyncSession = Depends(get_db),
    password_in: PasswordChange,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if not current_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have a password set (social login?).",
        )
    if not _hasher.verify(password_in.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    user = await user_service.update_user_password(
        db, db_user=current_user, new_password=password_in.new_password
    )
    return user


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar_me(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is not an image"
        )

    avatar_dir = "static/avatars"
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir)

    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{current_user.id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(avatar_dir, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    avatar_url = f"/static/avatars/{file_name}"
    user_in = UserUpdate(avatar_url=avatar_url)
    user = await user_service.update_user(db, db_user=current_user, user_in=user_in)
    return user


@router.post("/me/totp/setup", response_model=TOTPSetup)
async def setup_totp(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    secret = user_service.generate_totp_secret()
    uri = user_service.get_totp_uri(email=current_user.email, secret=secret)
    return {"secret": secret, "otpauth_url": uri}


@router.post("/me/totp/enable", response_model=UserResponse)
async def enable_totp(
    *,
    db: AsyncSession = Depends(get_db),
    verify_in: TOTPVerify,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if current_user.is_totp_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="TOTP is already enabled"
        )

    if not verify_in.secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Secret is required for first-time enablement",
        )

    if not verify_totp_code(verify_in.secret, verify_in.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid TOTP code"
        )

    user = await user_service.enable_totp(
        db, db_user=current_user, secret=verify_in.secret
    )
    return user


@router.post("/me/totp/disable", response_model=UserResponse)
async def disable_totp(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    user = await user_service.disable_totp(db, db_user=current_user)
    return user
