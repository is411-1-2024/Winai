from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

class TripDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id: int

app = FastAPI()

trip_db = []

@app.get("/trips/{trip_id}")
async def read_trip(trip_id: int) -> TripOut:
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == trip_id)
        trip = session.exec(statement).first()
        
        if trip != None:
            print(trip)
            return trip

    raise HTTPException(
        status_code=404, 
        detail="Trip not found"
    )

@app.get("/trips/")
async def read_trips() -> list[TripOut]:
    return trip_db

@app.post("/trips/")
async def create_trip(trip: Trip) -> TripOut:
    new_trip = {
        "id": len(trip_db)+1,
        **trip.model_dump(),
    }
        
    trip_db.append(new_trip)
    print(new_trip)
    return new_trip

@app.put("/trips/{trip_id}")
async def update_trip(trip_id: int, trip: Trip) -> TripOut:
    new_trip = {
        "id": trip_id,
        **trip.model_dump(),
    }

    for i in range(len(trip_db)):
        if trip_db[i]["id"] == trip_id:
            trip_db[i] = new_trip
            return new_trip
    
    raise HTTPException(
        status_code=404, 
        detail="Trip not found"
    )

@app.delete("/trips/{trip_id}")
async def delete_trip(trip_id: int):
    print("Deleting trip id {}".format(trip_id))

    for i in range(len(trip_db)):
        if trip_db[i]["id"] == trip_id:
            trip_db.pop(i)
            return { "message": "success" }

    raise HTTPException(
        status_code=404, 
        detail="Trip not found"
    )
