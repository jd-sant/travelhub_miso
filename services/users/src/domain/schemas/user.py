from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    correo_electronico: EmailStr
    telefono: str = Field(min_length=7, max_length=20)
    estado: int = Field(default=1, ge=0, le=1)


class UserCreate(UserBase):
    contrasena: str = Field(min_length=8)


class UserPublic(UserBase):
    id_usuario: UUID
