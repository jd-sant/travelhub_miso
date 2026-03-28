from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    correo_electronico: EmailStr
    telefono: str = Field(min_length=7, max_length=20)
    contrasena: str = Field(min_length=8)
    estado: int = Field(default=1, ge=0, le=1)


class UserResponse(BaseModel):
    id_usuario: UUID
    correo_electronico: str
    telefono: str
    estado: int
