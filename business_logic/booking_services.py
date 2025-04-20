from data_access.booking_dao import BookingDAO
from data_access.flight_dao import FlightDAO
from typing import Optional, Dict
from database.models import Booking


class BookingService:
    def __init__(self, session):
        self.booking_dao = BookingDAO(session)
        self.flight_dao = FlightDAO(session)

    def make_booking(self, flight_id: int, passenger_data: Dict, seat_class: str) -> Optional[Booking]:
        # Check flight availability
        flight = self.flight_dao.get_flight_by_id(flight_id)
        if not flight or flight.status != "Scheduled":
            return None

        # Calculate final price
        price = self.calculate_price(flight.base_price, seat_class)

        # Create booking
        booking = self.booking_dao.create_booking(flight_id, passenger_data, seat_class)
        if booking:
            booking.final_price = price
            self.booking_dao.session.commit()
        return booking

    def calculate_price(self, base_price: float, seat_class: str) -> float:
        multipliers = {
            "Economy": 1.0,
            "Premium Economy": 1.3,
            "Business": 1.8,
            "First Class": 2.5
        }
        return base_price * multipliers.get(seat_class, 1.0)

    def get_passenger_bookings(self, email: str):
        return self.booking_dao.get_bookings_by_passenger(email)