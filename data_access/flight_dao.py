from sqlalchemy.orm import Session
from typing import List, Optional
from database.models import Flight


class FlightDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_all_flights(self) -> List[Flight]:
        return self.session.query(Flight).order_by(Flight.departure_time).all()

    def get_flight_by_id(self, flight_id: int) -> Optional[Flight]:
        return self.session.query(Flight).filter(Flight.id == flight_id).first()

    def add_flight(self, flight: Flight) -> Flight:
        self.session.add(flight)
        self.session.commit()
        return flight

    def update_flight_status(self, flight_id: int, status: str) -> bool:
        flight = self.get_flight_by_id(flight_id)
        if flight:
            flight.status = status
            self.session.commit()
            return True
        return False