from sqlalchemy.orm import Session
from typing import List, Optional
from database.models import Booking, Passenger, Flight
from datetime import datetime


class BookingDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_booking(self, flight_id: int, passenger_data: dict, seat_class: str) -> Optional[Booking]:
        try:
            # Create passenger first
            passenger = Passenger(
                first_name=passenger_data['first_name'],
                last_name=passenger_data['last_name'],
                email=passenger_data['email'],
                phone=passenger_data['phone'],
                passport_number=passenger_data['passport_number']
            )
            self.session.add(passenger)
            self.session.flush()

            # Create booking
            booking = Booking(
                flight_id=flight_id,
                passenger_id=passenger.id,
                booking_date=datetime.now(),
                seat_class=seat_class,
                status="Confirmed"
            )
            self.session.add(booking)
            self.session.commit()
            return booking
        except Exception as e:
            self.session.rollback()
            print(f"Error creating booking: {e}")
            return None

    def get_bookings_by_passenger(self, email: str) -> List[Booking]:
        return self.session.query(Booking) \
            .join(Passenger) \
            .filter(Passenger.email == email) \
            .order_by(Booking.booking_date.desc()) \
            .all()

    def cancel_booking(self, booking_id: int) -> bool:
        booking = self.session.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            booking.status = "Cancelled"
            self.session.commit()
            return True
        return False