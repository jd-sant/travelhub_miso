from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from uuid import uuid4, UUID


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()

app = FastAPI(title="TravelHub Users Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID

    model_config = {"from_attributes": True}


# In-memory store for demonstration; replace with DB in production
USERS: dict[str, dict] = {}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "users-service"}


@app.get("/users", response_model=list[User])
def list_users():
    return list(USERS.values())


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    existing = next((u for u in USERS.values() if u["username"] == user_in.username), None)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_id = uuid4()
    user = {"id": user_id, **user_in.model_dump()}
    USERS[str(user_id)] = user
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID):
    user = USERS.get(str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user_in: UserCreate):
    if str(user_id) not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    user = {"id": user_id, **user_in.model_dump()}
    USERS[str(user_id)] = user
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID):
    if str(user_id) not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    del USERS[str(user_id)]
