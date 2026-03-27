from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.session import Session, create_db_and_tables, engine
from app.models.user import User
from sqlmodel import select

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}


router = api_router

__all__ = [
    "app",
    "router",
    "create_db_and_tables",
    "engine",
    "Session",
    "User",
    "select",
]
