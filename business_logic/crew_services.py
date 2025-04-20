from typing import List
from data_access.crew_dao import CrewDAO
from database.models import Crew


class CrewService:
    def __init__(self, session):
        self.dao = CrewDAO(session)

    def get_all_crew_members(self) -> List[Crew]:
        return self.dao.get_all_crew()

    def assign_crew_to_flight(self, crew_id: int, flight_id: int) -> bool:
        return self.dao.assign_crew_to_flight(crew_id, flight_id)