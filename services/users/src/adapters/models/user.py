from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(min_length=7, max_length=20)
    password: str = Field(min_length=8)
    status: int = Field(default=1, ge=0, le=1)
