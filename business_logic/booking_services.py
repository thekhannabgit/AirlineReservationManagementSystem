# business_logic/booking_services.py
from typing import Dict, Optional
from database.models import Booking, Flight, Passenger
from data_access.booking_dao import BookingDAO
from data_access.flight_dao import FlightDAO
from data_access.analytics_dao import AnalyticsDAO


class BookingService:
    def __init__(self, session):
        self.booking_dao = BookingDAO(session)
        self.flight_dao = FlightDAO(session)
        self.analytics_dao = AnalyticsDAO()

    def make_booking(self, flight_id: int, passenger_data: Dict, seat_class: str) -> Optional[Booking]:
        flight = self.flight_dao.get_flight_by_id(flight_id)
        if not flight or flight.status != "Scheduled":
            return None

        # Check seat availability
        if len(flight.bookings) >= flight.aircraft.capacity:
            return None

        # Calculate final price
        price = self.calculate_price(flight.base_price, seat_class)

        # Create booking
        booking = self.booking_dao.create_booking(
            flight_id=flight_id,
            passenger_data=passenger_data,
            seat_class=seat_class,
            price=price
        )

        if booking:
            # Log booking in analytics
            self.log_analytics(flight, booking)

        return booking

    def calculate_price(self, base_price: float, seat_class: str) -> float:
        multipliers = {
            "Economy": 1.0,
            "Premium Economy": 1.3,
            "Business": 1.8,
            "First Class": 2.5
        }
        return base_price * multipliers.get(seat_class, 1.0)

    def log_analytics(self, flight: Flight, booking: Booking):
        try:
            self.analytics_dao.log_booking({
                "flight_number": flight.flight_number,
                "route": f"{flight.departure_airport_code}-{flight.arrival_airport_code}",
                "price": booking.final_price,
                "seat_class": booking.seat_class,
                "passenger_email": booking.passenger.email
            })
        except Exception as e:
            print(f"Failed to log analytics: {str(e)}")