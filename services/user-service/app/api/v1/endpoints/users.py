from typing import Any

from app.api import deps
from app.models.user import User
from app.schemas.user import UserResponse
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
