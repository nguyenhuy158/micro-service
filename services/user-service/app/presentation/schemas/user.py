from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from shared.enums.status import UserRole


class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    full_name: str | None = None
    avatar_url: str | None = None
    role: UserRole | None = UserRole.CUSTOMER


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID | None = None


class UserResponse(UserInDBBase):
    is_totp_enabled: bool


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class TOTPSetup(BaseModel):
    secret: str
    otpauth_url: str


class TOTPVerify(BaseModel):
    code: str
    secret: str | None = None


class GoogleLogin(BaseModel):
    id_token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None
    role: str | None = None
