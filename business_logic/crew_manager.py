# business_logic/crew_manager.py
from data_access.models import Crew
from data_access.db_session import SessionLocal

def add_crew(name, role, flight_no):
    session = SessionLocal()
    crew = Crew(name=name, role=role, flight_number=flight_no)
    session.add(crew)
    session.commit()
    session.close()
