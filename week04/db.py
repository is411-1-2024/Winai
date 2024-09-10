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

with Session(engine) as session:
    statement = select(TripDB).where(TripDB.id == 20)
    trip = session.exec(statement).first()
    print(trip)

def create_data():
    trip_1 = TripDB(name='Sit still', destination='Home', duration=3, price=100.0, group_size=1)
    trip_2 = TripDB(name='Walk away', destination='Somewhere', duration=1, price=500.0, group_size=26)
    trip_3 = TripDB(name='Holidays', destination='Paradise', duration=999, price=1.0, group_size=2)

    with Session(engine) as session:
        session.add(trip_1)
        session.add(trip_2)
        session.add(trip_3)
        session.commit()