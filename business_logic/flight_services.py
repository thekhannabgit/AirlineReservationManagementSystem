from typing import List
from data_access.flight_dao import FlightDAO
from database.models import Flight


class FlightService:
    def __init__(self, session):
        self.dao = FlightDAO(session)

    def get_all_flights(self) -> List[Flight]:
        return self.dao.get_all_flights()

    def schedule_flight(self, flight_data: dict) -> Flight:
        from datetime import datetime
        flight = Flight(
            flight_number=flight_data['flight_number'],
            departure_airport_code=flight_data['departure_airport'],
            arrival_airport_code=flight_data['arrival_airport'],
            departure_time=datetime.strptime(flight_data['departure_time'], "%Y-%m-%d %H:%M"),
            arrival_time=datetime.strptime(flight_data['arrival_time'], "%Y-%m-%d %H:%M"),
            aircraft_id=flight_data['aircraft_id'],
            base_price=flight_data['base_price']
        )
        return self.dao.add_flight(flight)