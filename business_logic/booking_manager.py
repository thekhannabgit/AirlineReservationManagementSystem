# business_logic/booking_manager.py
from data_access.models import Booking, Passenger, Flight
from data_access.db_session import SessionLocal
import random

def book_flight(booking_ref, flight_no, name, email, phone):
    session = SessionLocal()
    flight = session.query(Flight).filter_by(flight_number=flight_no).first()
    if not flight:
        raise ValueError("Flight not found.")

    # Seat assignment (basic random logic)
    seat_number = f"{random.randint(1, flight.capacity)}A"

    passenger = Passenger(name=name, email=email, phone=phone)
    session.add(passenger)
    session.flush()

    booking = Booking(
        booking_ref=booking_ref,
        flight_id=flight.id,
        passenger_id=passenger.id,
        seat_number=seat_number
    )
    session.add(booking)
    session.commit()
    session.close()
