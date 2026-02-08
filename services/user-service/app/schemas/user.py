from uuid import UUID

from pydantic import BaseModel, EmailStr

from shared.enums.status import UserRole


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = True
    full_name: str | None = None
    role: UserRole | None = UserRole.CUSTOMER


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: UUID | None = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserResponse(UserInDBBase):
    pass


class GoogleLogin(BaseModel):
    id_token: str


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None
    role: str | None = None
