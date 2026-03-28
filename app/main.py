from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.session import create_db_and_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create schema once when the app process starts.
    create_db_and_tables()
    yield


def create_application() -> FastAPI:
    app = FastAPI(title="TravelHub Backend", lifespan=lifespan)
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"Hello": "World"}

    return app


app = create_application()
