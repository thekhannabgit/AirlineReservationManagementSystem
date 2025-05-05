# business_logic/flight_manager.py
from data_access.models import Flight
from data_access.db_session import SessionLocal
from datetime import datetime

def add_flight(flight_no, source, destination, departure_str, capacity):
    session = SessionLocal()
    departure_time = datetime.strptime(departure_str, "%Y-%m-%d %H:%M")
    flight = Flight(
        flight_number=flight_no,
        source=source,
        destination=destination,
        departure_time=departure_time,
        capacity=capacity
    )
    session.add(flight)
    session.commit()
    session.close()
