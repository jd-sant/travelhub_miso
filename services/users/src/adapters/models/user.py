from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id_usuario: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    correo_electronico: str = Field(index=True, unique=True)
    telefono: str = Field(min_length=7, max_length=20)
    contrasena: str = Field(min_length=8)
    estado: int = Field(default=1, ge=0, le=1)
