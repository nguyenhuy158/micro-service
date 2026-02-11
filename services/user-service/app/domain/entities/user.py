from uuid import UUID

from pydantic import BaseModel, EmailStr

from shared.enums.status import UserRole


class UserEntity(BaseModel):
    id: UUID | None = None
    email: EmailStr
    hashed_password: str | None = None
    full_name: str | None = None
    is_active: bool = True
    google_id: str | None = None
    avatar_url: str | None = None
    totp_secret: str | None = None
    is_totp_enabled: bool = False
    role: UserRole = UserRole.CUSTOMER

    model_config = {"from_attributes": True}
