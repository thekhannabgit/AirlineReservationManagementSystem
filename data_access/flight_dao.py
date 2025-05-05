# data_access/flight_dao.py
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from database.models import Flight, Airport, Aircraft, Booking, FlightStatus
#from database.enums import FlightStatus


class FlightDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_all_flights(self) -> List[Flight]:
        """Get all flights ordered by departure time"""
        return self.session.query(Flight) \
            .order_by(Flight.departure_time) \
            .all()

    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        """Get a single flight by ID"""
        return self.session.query(Flight) \
            .filter(Flight.id == flight_id) \
            .first()

    def get_flights_by_route(self,
                             departure: str,
                             arrival: str,
                             date: datetime = None) -> List[Flight]:
        """Get flights between two airports, optionally filtered by date"""
        query = self.session.query(Flight) \
            .join(Airport, Flight.departure_airport_code == Airport.code) \
            .filter(
            Flight.departure_airport_code == departure,
            Flight.arrival_airport_code == arrival,
            Flight.status == FlightStatus.SCHEDULED
        )

        if date:
            start_date = date.replace(hour=0, minute=0, second=0)
            end_date = start_date + timedelta(days=1)
            query = query.filter(
                Flight.departure_time >= start_date,
                Flight.departure_time < end_date
            )

        return query.order_by(Flight.departure_time).all()

    def get_available_flights(self,
                              from_date: datetime = None,
                              to_date: datetime = None) -> List[Flight]:
        """Get available flights within a date range"""
        query = self.session.query(Flight) \
            .join(Aircraft) \
            .filter(
            Flight.status == FlightStatus.SCHEDULED,
            Flight.departure_time > datetime.now()
        )

        if from_date:
            query = query.filter(Flight.departure_time >= from_date)
        if to_date:
            query = query.filter(Flight.departure_time <= to_date)

        return query.order_by(Flight.departure_time).all()

    def add_flight(self, flight: Flight) -> Flight:
        """Add a new flight to the database"""
        try:
            self.session.add(flight)
            self.session.commit()
            return flight
        except Exception as e:
            self.session.rollback()
            raise e

    def update_flight_status(self, flight_id: int, status: FlightStatus) -> bool:
        """Update flight status"""
        flight = self.get_flight_by_id(flight_id)
        if flight:
            flight.status = status
            self.session.commit()
            return True
        return False

    def get_flight_occupancy(self, flight_id: int) -> Tuple[int, int]:
        """Get booked and total seats for a flight"""
        flight = self.session.query(Flight) \
            .join(Aircraft) \
            .filter(Flight.id == flight_id) \
            .first()

        if not flight:
            return (0, 0)

        booked_seats = self.session.query(func.count(Booking.id)) \
            .filter(Booking.flight_id == flight_id) \
            .scalar()

        return (booked_seats, flight.aircraft.capacity)

    def search_flights(self,
                       departure: str = None,
                       arrival: str = None,
                       date: datetime = None) -> List[Flight]:
        """Search flights with optional filters"""
        query = self.session.query(Flight) \
            .join(Airport, Flight.departure_airport_code == Airport.code) \
            .filter(Flight.status == FlightStatus.SCHEDULED)

        if departure:
            query = query.filter(Flight.departure_airport_code == departure)
        if arrival:
            query = query.filter(Flight.arrival_airport_code == arrival)
        if date:
            start_date = date.replace(hour=0, minute=0, second=0)
            end_date = start_date + timedelta(days=1)
            query = query.filter(
                Flight.departure_time >= start_date,
                Flight.departure_time < end_date
            )

        return query.order_by(Flight.departure_time).all()