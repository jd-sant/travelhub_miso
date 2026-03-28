from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    password: str = Field(min_length=8)
    status: int = Field(default=1, ge=0, le=1)


class UserResponse(BaseModel):
    id: UUID
    email: str
    phone: str
    status: int
