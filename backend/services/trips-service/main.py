from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from uuid import uuid4, UUID
from datetime import date


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()

app = FastAPI(title="TravelHub Trips Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripBase(BaseModel):
    name: str
    destination: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    price: float


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: UUID

    model_config = {"from_attributes": True}


# In-memory store for demonstration; replace with DB in production
TRIPS: dict[str, dict] = {}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "trips-service"}


@app.get("/trips", response_model=list[Trip])
def list_trips():
    return list(TRIPS.values())


@app.post("/trips", response_model=Trip, status_code=status.HTTP_201_CREATED)
def create_trip(trip_in: TripCreate):
    trip_id = uuid4()
    trip = {"id": trip_id, **trip_in.model_dump()}
    TRIPS[str(trip_id)] = trip
    return trip


@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: UUID):
    trip = TRIPS.get(str(trip_id))
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@app.put("/trips/{trip_id}", response_model=Trip)
def update_trip(trip_id: UUID, trip_in: TripCreate):
    if str(trip_id) not in TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip = {"id": trip_id, **trip_in.model_dump()}
    TRIPS[str(trip_id)] = trip
    return trip


@app.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: UUID):
    if str(trip_id) not in TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    del TRIPS[str(trip_id)]
