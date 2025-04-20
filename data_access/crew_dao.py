from sqlalchemy.orm import Session
from typing import List
from database.models import Crew


class CrewDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_all_crew(self) -> List[Crew]:
        return self.session.query(Crew).all()

    def assign_crew_to_flight(self, crew_id: int, flight_id: int) -> bool:
        # Implementation here
        pass