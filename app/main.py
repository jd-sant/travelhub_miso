from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.session import create_db_and_tables


def create_application() -> FastAPI:
    app = FastAPI(title="TravelHub Backend")
    app.include_router(api_router, prefix="/api/v1")
    create_db_and_tables()

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {"Hello": "World"}

    return app


app = create_application()
